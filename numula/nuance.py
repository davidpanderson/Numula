# functions for expressing nuance
# see https://github.com/davidpanderson/Numula/wiki/nuance.py

import numpy, random, copy, math
from numula.nscore import *
from numula.pft import *

# modes for adjust_tempo_pft()
#
TIME_TEMPO = 0
    # larger is faster; use integral_inverse()
TIME_PSEUDO_TEMPO = 1
    # larger is faster; invert params, use integral()
TIME_SLOWNESS = 2
    # larger is slower; use integral()

# ------------------- Dynamics ------------------------

# modes for vol_adjust_pft() and other dynamic functions
#
VOL_MULT = 0
VOL_ADD = 1
VOL_SET = 2

# derived Score class adds member functions for nuance

class Score(ScoreBasic):
    # adjust or set volume of selected notes by PFT starting at t0
    def vol_adjust_pft(
        self, pft:PFT, t0:float=0, selector:Selector=None, mode:int=VOL_MULT
    ):
        if not pft: return
        self.time_sort()
        self.tags_init()
        pft_check_closure(pft)
        seg_ind = 0
        seg = pft[0]
            # which segment we're on
        seg_start = t0
            # start time of that segment
        seg_end = t0 + seg.dt
        t_end = t0 + pft_dur(pft)
            # end time of PFT
        for n in self.notes:
            if n.time > t_end + epsilon:
                break
            if n.time < t0 - epsilon:
                continue
            if selector and not selector(n):
                continue
            while True:
                # skip segments as needed
                if n.time < seg_end - epsilon:
                    v = seg.val(n.time - seg_start)
                    break
                if n.time < seg_end + epsilon:
                    # note is at end of this seg
                    if seg.closed_end:
                        v = seg.y1
                        break
                    if seg_ind == len(pft)-1:
                        return
                # move to next seg
                seg_start += seg.dt
                seg_ind += 1
                seg = pft[seg_ind]
                seg_end = seg_start + seg.dt
            # v is the adjustment factor
            if mode == VOL_MULT:
                n.vol *= v
            elif mode == VOL_ADD:
                n.vol += v
            elif mode == VOL_SET:
                if v < 0:
                    continue
                n.vol = v/2
            
    def vol_adjust(self, v:float, selector:Selector=None, mode:int=VOL_MULT):
        self.tags_init()
        for n in self.notes:
            if selector and not selector(n):
                continue
            if mode == VOL_MULT:
                n.vol *= v
            elif mode == VOL_ADD:
                n.vol += v
            elif mode == VOL_SET:
                n.vol = v/2
                
    def vol_adjust_func(
        self, func:NoteToFloat, selector:Selector=None, mode:int=VOL_MULT
    ):
        self.tags_init()
        for n in self.notes:
            if selector and not selector(n):
                continue
            v = func(n)
            if mode == VOL_MULT:
                n.vol *= v
            elif mode == VOL_ADD:
                n.vol += v
            elif mode == VOL_SET:
                n.vol = v/2

    # randomly perturb volume
    #
    def v_random_uniform(self, min:float, max:float, selector:Selector=None):
        self.tags_init()
        for note in self.notes:
            if selector and not selector(note): continue
            note.vol *= random.uniform(min, max)

    def v_random_normal(
        self, stddev:float, max_sigma:float=2, selector:Selector=None
    ):
        self.tags_init()
        for note in self.notes:
            if selector and not selector(note): continue
            while True:
                x = numpy.random.normal()
                if abs(x) < max_sigma: break
            note.vol *= 1+stddev*x

# ------------------- Timing ------------------------

    # perf time is score time * 240/tempo
    # so the integral of the PFT is scaled by this.
    # If we want to add a pause (in seconds) to the integral
    # we need to undo this scaling first.
    #
    def dt_to_integral(self, dt: float) -> float:
        return dt*self.tempo/240.
        
    # Apply the PFT, starting at score time t0, to the selected notes.
    # and to all pedal events.
    # pft is a tempo function,
    # which can contain segments (e.g. Linear) and Pauses
    # modes:
    # TIME_INVERSE_TEMPO
    #   PFT value is performance time per unit score time; larger is slower.
    # TIME_TEMPO
    #   use integral_inverse(); larger is faster
    #   (60 = no change, 120 = speed up by 2X)
    # TIME_PSEUDO_TEMPO
    #   invert tempo params of segments; larger is faster.
    #   Use this if some segments don't have integral_inverse()
    # In all modes, the value of Pauses is performance time.
    #
    # If "normalize" is True, scale the PFT so that its average is 1.
    #
    # Implementation:
    # 1)    make a time-sorted list of start/end "events"
    #       for the notes and pedals,
    #       each with (score) time and a perf time.
    # 2)    for each successive pair of events A and B,
    #       compute average of the PFT between the score times of A and B.
    #       scale the perf time interval between A and B by this.
    # 3)    update the (perf) time and dur of the corresponding
    #       Note and Pedal objects.
    #
    def tempo_adjust_pft(self,
        _pft:PFT, t0:float=0.,
        selector:Selector=None, normalize:bool=False,
        mode:int=TIME_PSEUDO_TEMPO,
        debug:bool=False
    ):
        self.init_all()
        if mode == TIME_PSEUDO_TEMPO:
            pft = copy.deepcopy(_pft)
            pft_bpm(pft)    # invert tempo function, making it slowness
        else:
            pft = copy.copy(_pft)

        if debug:
            print('after BPM:')
            print(*pft, sep='\n')
            #print('PFT values:')
            #show_pft_vals(pft, 1/16)
            #print('PFT integrals:')
            #show_pft_ints(pft, 1/16)

        scale_factor = 1.0
        if normalize:
            # the PFT consists of segments (tempo functions) and Delays.
            # To compute the scale factor we have to compute
            # the total effect of both.
            pftd = pft_dur(pft)
            delay = pft_delay(pft)
            y = pftd*pft_avg(pft) + self.dt_to_integral(delay)
            scale_factor = pftd/y

        # append infinite unity segment
        # needed to handle events that lie beyond PFT domain
        if mode == TIME_SLOWNESS:
            pft.append(Unity(9999999))
        else:
            pft.append(Linear(60, 60, 9999999))
        
        self.make_start_end_events()

        # keep track of our position in the PFT, and the integral so far
        #
        seg_ind = 0
        seg = pft[0]
        seg_start = t0
        seg_end = t0 + seg.dt
        seg_integral = 0        # integral up to current seg

        # keep track of params of previous event
        #
        prev_time = -999    # its score time
        prev_perf = 0       # its perf time
        prev_perf_adj = 0   # its adjusted perf time
        prev_integral = 0   # integral of PFT at that point

        # add the current PFT segment's integral to seg_integral
        # and advance to the next segment
        # 
        def advance_seg():
            nonlocal seg_start, seg_integral, seg_ind, seg, seg_end, mode
            seg_start += seg.dt
            if seg.dt == 0:
                si = self.dt_to_integral(seg.value)
            else:
                if mode == TIME_TEMPO:
                    si = 60*seg.integral_inverse(seg.dt)
                else:
                    si = seg.integral(seg.dt)
            seg_integral += si
            if debug:
                print('    moving to next seg')
            seg_ind += 1
            seg = pft[seg_ind]
            if debug:
                if mode == TIME_TEMPO:
                    si = 60*seg.integral_inverse(seg.dt)
                else:
                    si = seg.integral(seg.dt)
                print('    next segment: dt %f integral %f'%(seg.dt, si))
            seg_end = seg_start + seg.dt

        # the event lies in the current segment.
        # Compute the integral at the event time, and compute its perf time
        #
        def use_seg():
            nonlocal prev_integral, prev_time, prev_perf, prev_perf_adj
            if debug:
                print('    use_seg(): dt', seg.dt)
            if seg.dt == 0:
                si = self.dt_to_integral(seg.value)
            else:
                if mode == TIME_TEMPO:
                    si = 60*seg.integral_inverse(event.time - seg_start)
                else:
                    si = seg.integral(event.time - seg_start)
            i = seg_integral + si
                # integral of pft at this point
            if debug:
                print('    i = seg_integral + si')
                print('    %f = %f + %f '%(
                    i, seg_integral, si
                ))
            d = i - prev_integral
                # integral since previous event
            if debug:
                print('    d = i - prev_integral')
                print('    %f = %f - %f'%(d, i, prev_integral))
            avg = scale_factor*d/(event.time - prev_time)
                # average tempo since prev event
            if debug:
                print('    avg = scale_factor*d/(event.time - prev_time)')
                print('    %f = %f*%f/(%f-%f)'%(
                    avg, scale_factor, d, event.time, prev_time
                ))
            dperf = event.perf_time - prev_perf
            prev_perf = event.perf_time
            new_perf = prev_perf_adj + dperf*avg
            if debug:
                print('    new perf = prev_perf_adj + dperf*avg')
                print('   ', new_perf, '=', prev_perf_adj, '+', dperf,'*', avg)
            event.perf_time = new_perf
            prev_perf_adj = event.perf_time
            prev_integral = i
            if debug:
                print('    new PFT integral %f; int since prev event %f; score time dt %f; int avg %f'%(
                    i, d, event.time-prev_time, avg
                ))
                print('    changed perf delay from %f to %f'%(
                    dperf, dperf*avg
                ))
            prev_time = event.time

        # loop over events
        #
        for event in self.start_end:
            # skip if event is before start of PFT
            #
            if event.time < t0-epsilon:
                continue

            # if the time adjustment is normalized,
            # by definition everything after it is unaffected
            #
            if normalize and event.time > t0+pftd-epsilon:
                break

            if debug:
                print('event: time %f perf time %f prev_time %f'%(
                    event.time, event.perf_time, prev_time)
                )

            # skip if event is not selected
            #
            if selector:
                if event.kind == event_kind_note:
                    if not selector(event.obj):
                        if debug:
                            print('  not selected')
                        continue

            # same score time as prev event, use same perf time
            #
            if event.time - prev_time < epsilon:
                if debug:
                    print('  same score time as prev; set perf time to %f'%prev_perf_adj)
                event.perf_time = prev_perf_adj
                continue

            # if event is at the start of the PFT, handle specially.
            #
            if event.time < t0+epsilon:
                if debug:
                    print('   Handling event at start of PFT');
                prev_time = event.time
                prev_perf = event.perf_time
                # is first segment a pause-before?
                #
                if seg.dt==0 and not seg.after:
                    if debug:
                        print('   Handling pause-before at start of PFT');
                    event.perf_time += seg.value
                    prev_integral = self.dt_to_integral(seg.value)
                    advance_seg() 
                else:
                    prev_integral = 0
                prev_perf_adj = event.perf_time
                continue

            # if there's no event at the start of the PFT, pretend there's one
            #
            if prev_time < 0:
                prev_time = 0
                if debug:
                    print('tempo PFT does not start at note')

            # loop over PFT segments until last one that affects the event, i.e. either
            # E lies strictly within S, or
            # E is at the endpoint of S and the next seg is not a before-Pause
            # precondition: event.time is not strictly before current seg
            while True:
                if debug:
                    print('  Seg loop: seg_start', seg_start, ' seg_end', seg_end, ' seg integral', seg_integral)
                if event.time < seg_end - epsilon:
                    if debug: print('   event is strictly in seg; using it')
                    use_seg()
                    break
                elif event.time < seg_end + epsilon:
                    if debug: print('    event is at end of seg')
                    next_seg = pft[seg_ind+1]
                    if next_seg.dt > 0:
                        if debug: print('    next seg not Pause; using and advancing')
                        use_seg()
                        advance_seg()
                        break
                    else:
                        if next_seg.after:
                            if debug: print('    next seg is after-Pause: use and advance')
                            use_seg()
                            advance_seg()
                            break
                        if debug: print('    next seg is before-Pause: advance')
                advance_seg()
            if debug:
                print('  Done with event: perf time ', event.perf_time)
        # end loop over events
        self.transfer_start_end_events()

    # Note shifting (e.g. for agogic accents)
    # shift start time of selected notes by the PFT value
    #
    def time_shift_pft(self, pft:PFT, t0:float=0, selector:Selector=None):
        if not pft:
            return
        self.init_all()
        pft_check_closure(pft)
        seg_ind = 0
        seg = pft[0]
            # which segment we're on
        seg_start = t0
            # start time of that segment
        seg_end = t0 + seg.dt
        t_end = t0 + pft_dur(pft)
            # end time of function
        for n in self.notes:
            if n.time > t_end + epsilon:
                break
            if n.time < t0 - epsilon:
                continue
            if selector and not selector(n):
                continue
            while True:
                # skip segments as needed
                if n.time < seg_end - epsilon:
                    v = seg.val(n.time - seg_start)
                    break
                if n.time < seg_end + epsilon:
                    # note is at end of this seg
                    if seg.closed_end:
                        v = seg.y1
                        break
                    if seg_ind == len(pft)-1:
                        return
                # move to next seg
                seg_start += seg.dt
                seg_ind += 1
                seg = pft[seg_ind]
                seg_end = seg_start + seg.dt
            # v is the shift factor
            if v == 0:
                continue
            n.perf_time += v
            n.perf_dur -= v

    # change dur of notes starting between t0 and t1 so they end at t1
    # (like a local sustain pedal)
    def sustain(self, t0:float, t1:float, selector:Selector=None):
        self.time_sort()
        if selector:
            self.tags_init()
        for n in self.notes:
            if n.time<t0 - epsilon:
                continue
            if n.time > t1:
                break
            if selector and not selector(n):
                continue
            end = n.time + n.dur
            if end < t1:
                n.dur = t1 - n.time

    # insert a pause of dt before time t.
    # If connect is True, extend earlier notes ending at t to preserve legato

    @staticmethod
    def pb_aux(items, t, dt, connect):
        for item in items:
            if item.time + item.dur < t-epsilon:
                # note ends before t
                continue
            if item.time < t-epsilon:
                # note starts before t and ends t or later
                if connect:
                    item.perf_dur += dt
            else:
                # note starts t or later
                item.perf_time += dt

    def pause_before(self, t:float, dt:float, connect:bool=True):
        self.init_all()
        self.pb_aux(self.notes, t, dt, connect)
        self.pb_aux(self.pedals, t, dt, connect)

    # pause after notes at t.
    @staticmethod
    def pa_aux(items, t, dt):
        for item in items:
            if item.time < t-epsilon:
                # note starts before t
                if item.time + item.dur > t + epsilon:
                    # not ends after t - elongate it
                    item.perf_dur += dt
                continue
            if item.time > t+epsilon:
                # note starts after t
                item.perf_time += dt
            else:
                # note starts at t
                item.perf_dur += dt

    def pause_after(self, t:float, dt:float):
        self.init_all()
        self.pa_aux(self.notes, t, dt)
        self.pa_aux(self.pedals, t, dt)
                    
    # insert a list of pauses with gaps.
    # ts = times when gaps occur
    # dts = lengths of gaps
    # like a bunch of calls to pause_before(..., connect=False)
    # but more efficient because we do one pass through the score.
    # Note: tempo_adjust_pft() can insert pauses, but not gaps

    @staticmethod
    def pbl_aux(items, ts, dts):
        ind = 0
        cur_t = ts[0]
        dt_sum = 0
        for item in items:
            if item.time < cur_t - epsilon:
                # note is before current gap
                item.perf_time += dt_sum
            elif item.time < cur_t + epsilon:
                # note is at current gap
                item.perf_time += dt_sum + dts[ind]
            else:
                # note is after current gap
                # scan gaps before note
                dt_sum += dts[ind]
                while True:
                    ind += 1
                    if ind == len(ts):
                        cur_t = 1e9
                        item.perf_time += dt_sum
                        break
                    cur_t = ts[ind]
                    if cur_t < item.time-epsilon:
                        dt_sum += dts[ind]
                        continue
                    elif cur_t < item.time+epsilon:
                        item.perf_time += dt_sum + dts[ind]
                        break
                    else:
                        item.perf_time += dt_sum
                        break

    def pause_before_list(self, ts, dts):
        self.init_all()
        if len(ts) == 0:
            raise Exception('empty time list')
        if len(ts) != len(dts):
            raise Exception('lists are different sizes')
        self.pbl_aux(self.notes, ts, dts)
        self.pbl_aux(self.pedals, ts, dts)

    @staticmethod
    def roll_aux(chord:list[Note], offsets:list[float], is_up:bool):
        if is_up:
            chord.sort(key=lambda x: x.pitch)
        else:
            chord.sort(key=lambda x: -x.pitch)
        ind = 0
        while ind < len(chord) and ind < len(offsets):
            note = chord[ind]
            off = offsets[ind]
            note.perf_time += off
            note.perf_dur -= off
            if note.perf_dur < epsilon:
                raise Exception('roll amount exceeds note duration')
            ind += 1

    def roll(self,
        t:float, offsets:list[float], is_up:bool=True,
        selector:Selector=None, verbose:bool=False
    ):
        self.init_all()
        chord = []   # the notes at time t
        for note in self.notes:
            if note.time < t-epsilon:
                continue
            if note.time > t+epsilon:
                break
            if selector and not selector(note):
                continue
            chord.append(note)
        if chord:
            if verbose:
                print('roll ', offsets, list(map(lambda n: n.pitch, chord)))
            self.roll_aux(chord, offsets, is_up)

    def t_adjust_list(self, offsets:list[float], selector:Selector):
        self.init_all()
        ind = 0
        for note in self.notes:
            if ind == len(offsets):
                break
            if selector and not selector(note):
                continue
            note.perf_time += offsets[ind]
            ind += 1

    def t_adjust_notes(self, offset:float, selector:Selector):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.perf_time += offset

    def t_adjust_func(self, func:NoteToFloat, selector:Selector):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.perf_time += func(note)

    # perturb start time, and adjust duration to keep end time the same
    # Possible TODO: adjust durations of earlier notes that end at this time
    #
    def t_random_uniform(self, min:float, max:float, selector:Selector=None):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            x = random.uniform(min, max)
            note.perf_time += x
            note.perf_dur -= x

    def t_random_normal(self,
        stddev:float, max_sigma:float=2, selector:Selector=None
    ):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            while True:
                x = numpy.random.normal()
                if abs(x) < max_sigma:
                    break
            y = stddev*x
            note.perf_time += y
            note.perf_dur -= y
                    
# --------------- Articulation ----------------------

    def score_dur_abs(self, dur:float, selector:Selector=None):
        self.tags_init()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.dur = dur

    def score_dur_rel(self, factor:float, selector:Selector=None):
        self.tags_init()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.dur *= factor

    def score_dur_func(self, func:NoteToFloat, selector:Selector=None):
        self.tags_init()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.dur = func(note)
 
    def perf_dur_abs(self, dur:float, selector:Selector=None):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.perf_dur = dur

    def perf_dur_rel(self, factor:float, selector:Selector=None):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.perf_dur *= factor

    def perf_dur_func(self, func:NoteToFloat, selector:Selector=None):
        self.init_all()
        for note in self.notes:
            if selector and not selector(note):
                continue
            note.perf_dur = func(note)

    # adjust articulation with a PFT
    def perf_dur_pft(self,
        pft:PFT, t0:float, selector:Selector=None, rel:bool=True
    ):
        self.init_all()
        pft_check_closure(pft)
        seg_ind = 0
        seg = pft[0]
            # which segment we're on
        seg_start = t0
            # start time of that segment
        seg_end = t0 + seg.dt
        t_end = t0 + pft_dur(pft)
            # end time of function
        for n in self.notes:
            if n.time > t_end + epsilon:
                break
            if n.time < t0 - epsilon:
                continue
            if selector and not selector(n):
                continue
            while True:
                # skip segments as needed
                if n.time < seg_end - epsilon:
                    v = seg.val(n.time - seg_start)
                    break
                if n.time < seg_end + epsilon:
                    # note is at end of this seg
                    if seg.closed_end:
                        v = seg.y1
                        break
                    if seg_ind == len(pft)-1:
                        return
                # move to next seg
                seg_start += seg.dt
                seg_ind += 1
                seg = pft[seg_ind]
                seg_end = seg_start + seg.dt
            # v is the adjustment factor
            if rel:
                n.perf_dur *= v
            else:
                n.perf_dur = v

# ----------- pedals -------------

    # apply a virtual sustain PFT:
    # extend the (score) duration of affected notes
    def vsustain_pft(self,
        pft:PFT, t0:float=0, selector:Selector=None, verbose:bool=False
    ):
        self.time_sort()
        # this changes score time.
        # If we've already transferred score time to perf time,
        # those changes will be lost.
        if self.perf_inited:
            raise Exception('vsustain_pft() must precede tempo adjustment')

        seg_ind = 0
        seg = pft[0]
        seg_start = t0
        seg_end = t0 + seg.dt
        t_end = t0 + pft_dur(pft)
        vstr = ''
        for n in self.notes:
            if verbose:
                vstr += 'vsus: %s\n'%n.__str__()
            if n.time > t_end + epsilon:
                break
            if n.time < t0 - epsilon:
                continue
            if selector and not selector(n):
                continue
            while True:
                if n.time < seg_end - epsilon:
                    if seg_end > n.time + n.dur:
                        if seg.level0 > 0:
                            if verbose:
                                vstr += 'vsus: elongating note\n'
                            n.dur = seg_end - n.time
                    break
                seg_ind += 1
                if seg_ind == len(pft):
                    return
                seg_start += seg.dt
                seg = pft[seg_ind]
                seg_end = seg_start + seg.dt
        if verbose:
            print(vstr)

    # apply a pedal PFT (sustain, sostenuto, or soft)
    def pedal_pft(self, pft:PFT, type:int=PEDAL_SUSTAIN, t0:float=0):
        t = t0
        for seg in pft:
            seg.time = t
            seg.type = type
            self.insert_pedal(seg)
            t += seg.dt

# ----------- spatialization ----------------

    # return array of per-frame stereo positions -1..1,
    # based on a PFT defining position as a function of score time.
    # If the performance times exceed the PFT,
    # use the final PFT value for those frames
    #
    def get_pos_array(self, pos_pft:PFT, framerate:float) -> list[float]:
        # get the score's note start/end events.
        # Then extract a subset which is strictly monotonic
        # in both score and performance time.
        # This defines a piecewise linear function F
        # mapping perf time to score time.
        # The stereo position at a given frame (perf time t)
        # is the value of pos_pft at score time F(t)
        #
        self.make_start_end_events()
        last_time = 0.
        last_perf_time = 0.
        events: list[Event] = []
        # events are sorted by score time
        for event in self.start_end:
            if event.time <= last_time:
                continue
            if event.perf_time <= last_perf_time:
                continue
            events.append(event)
            last_time = event.time
            last_perf_time = event.perf_time

        # make an object for evaluating pos_pft at increasing times
        pft_val = PFTValue(pos_pft)
        event_ind = 0
        ev0 = events[0]
        ev1 = events[1]
        slope = (ev1.time - ev0.time)/(ev1.perf_time - ev0.perf_time)
        nframes = math.ceil(last_perf_time*framerate)
        pos_array = [0.]*nframes
        print('get_pos_array: nframes', nframes)
        for i in range(nframes):
            pt = i/framerate
            # loop over linear segments of F
            while pt > ev1.perf_time:
                event_ind += 1
                ev0 = events[event_ind]
                ev1 = events[event_ind+1]
                slope = (ev1.time - ev0.time)/(ev1.perf_time - ev0.perf_time)
            t = ev0.time + (pt-ev0.perf_time)*slope
            if pft_val.ended:
                pos = pft_val.final_value
            else:
                pos = pft_val.value(t)
            pos_array[i] = pos
        return pos_array
