# This file is part of Numula
# Copyright (C) 2023 David P. Anderson
#
# Numula is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Numula is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Numula.  If not, see <http://www.gnu.org/licenses/>.

# functions for expressing nuance
# see https://github.com/davidpanderson/Numula/wiki/nuance.py

import numpy, random, copy, math
from numula.nscore import *

# -------- PFT (piecewise function of time) primitives ----------

class Linear:
    def __init__(self, y0, y1, dt, closed_start=True, closed_end=False):
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.closed_start = closed_start
        self.closed_end = closed_end
    def __str__(self):
        return 'Linear: %s %f %f %s, dt %f'%(
            '[' if self.closed_start else '(',
            self.y0, self.y1,
            ']' if self.closed_end else ')',
            self.dt
        )
    def val(self, t):
        return self.y0 + self.dy*(t/self.dt)
    def integral(self, t):
        return t*(self.y0+self.val(t))/2
    def integral_total(self):
        return self.dt*(self.y0+self.y1)/2
    # convert from tempo function in BPM (60-centered)
    # to 1-centered inverse tempo function
    def bpm(self):
        self.y0 = 60/self.y0
        self.y1 = 60/self.y1
        self.dy = self.y1 - self.y0

# for volume PFTs: a period of unity gain
#
def Unity(dt):
    return Linear(1, 1, dt)

# for time-shift PFTs: a period of no shift
#
def ZeroSeg(dt):
    return Linear(0, 0, dt)

# for volume and time-shift PFTs: a momentary value
#
class Accent:
    def __init__(self, y):
        self.y0 = y
        self.y1 = y
        self.closed_start = True
        self.closed_end = True
        self.dt = 0
    def __str__(self):
        return 'Accent %f'%self.y0
    def val(self, t):
        return y0
    
# An exponential parameterized by "curvature".
# Normalized to 0..1 for both x and y, the value is
# y = (1 - c^x)/(1-c)
# where c is e^curvature
# If curvature > 0 more of the change happens later;
# i.e. if y1 > y0 then the curve is concave up
# and if curvature < 0 more of the change happens earlier.
# If curvature = 0 then y = x; this is handled as a special case
class ExpCurve:
    def __init__(self, curvature, y0, y1, dt, closed_start=True, closed_end=False):
        if abs(curvature) < .001:
            self.linear = True
        else:
            self.linear = False
            self.c = math.exp(curvature)
            self.logc = curvature
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.closed_start = closed_start
        self.closed_end = closed_end
        self.curvature = curvature
    def __str__(self):
        return 'ExpCurve: %s %f %f %s, dt %f curvature %f'%(
            '[' if self.closed_start else '(',
            self.y0, self.y1,
            ']' if self.closed_end else ')',
            self.dt, self.curvature
        )       
    def val(self, t):
        if self.linear:
            return self.y0 + self.dy*(t/self.dt)
        tnorm = t/self.dt
        ynorm = (1 - math.pow(self.c, tnorm))/(1-self.c)
        return self.y0 + ynorm*self.dy
    def integral(self, t):
        if self.linear:
            return t*(self.y0+self.val(t))/2
        if t == 0:
            return 0
        # I assume you know that the integral of a^x is a^x/ln(a) + C
        # (OK, so I had to look it up)
        #
        tnorm = t/self.dt

        a = (math.pow(self.c, tnorm) - 1)/self.logc

        int_norm = (tnorm-a)/(1-self.c)

        # convert from normalized coords
        int = t*(self.y0 + int_norm*self.dy)
        #print('integral: ', t, int_norm, self.dy, int)
        return int
    def integral_total(self):
        if self.linear:
            return self.dt*(self.y0+self.y1)/2
        return self.integral(self.dt)
    def bpm(self):
        self.y0 = 60/self.y0
        self.y1 = 60/self.y1
        self.dy = self.y1 - self.y0

# Dirac delta; used in tempo PFTs to represent pauses
# if after is True, pause goes after notes at that time
class Delta:
    def __init__(self, value, after=True):
        self.value = value
        self.after = after
        self.dt = 0
    def __str__(self):
        return 'Delta %f %s'%(
            self.value,
            'after' if self.after else 'before'
        )
    def bpm(self):
        return
    def integral_total(self):
        return self.value

# a pedal PFT is a list of these.
# level 0 is a period of no pedal
# pedal types don't have to all be the same
class PedalSeg:
    def __init__(self, dt, level, pedal_type=pedal_sustain):
        self.dt = dt
        self.level = level
        self.pedal_type = pedal_type
    def __str__(self):
        return 'PedalSeg: dt %f type %d level %f'%(
            self.dt, self.pedal_type, self.level
        )

# a PFT segment whose value is an arbitrary object (e.g. a PitchSet)
#
class PFTObject:
    def __init__(self, dt, value, closed_start=True, closed_end=False):
        self.dt = dt
        self.y0 = value
        self.y1 = value
        self.closed_start = closed_start
        self.closed_end = closed_end
    def val(self, t):
        return self.y0

# ------------ end of PFT primitives

#from pprint import pprint

# make sure the pft has well-defined values at segment boundaries
def pft_check_closure(pft):
    n = len(pft)
    t = 0
    for i in range(n-1):
        seg0 = pft[i]
        t += seg0.dt
        seg1 = pft[i+1]
        if isinstance(seg0, Accent):
            seg1.closed_start = False
            continue
        if isinstance(seg1, Accent):
            seg0.closed_end = False
            continue
        if seg0.closed_end:
            if seg1.closed_start and seg0.y1 != seg1.y0:
                raise Exception('conflicting values in PFT at time %f'%t)
        else:
            if not seg1.closed_start:
                raise Exception('missing value in PFT at time %f'%t)

# score-time duration of a PFT
def pft_dur(pft):
    dt = 0
    for seg in pft:
        dt += seg.dt
    return dt

# verify that the PFT has the given duration
def pft_verify_dur(pft, dur):
    x = pft_dur(pft)
    if x < dur-epsilon:
        raise Exception('PFT is too short: %f < %f'%(x, dur))
    if x > dur+epsilon:
        raise Exception('PFT is too long: %f > %f'%(x, dur))
    
# average value of pft
def pft_avg(pft):
    sum = 0
    for seg in pft:
        sum += seg.integral_total()
    return sum/pft_dur(pft)

# convert tempo PFT from BPM units
def pft_bpm(pft):
    for seg in pft:
        seg.bpm()

# class for getting the values of a PFT at increasing times
class PFTValue:
    def __init__(self, pft):
        self.pft = pft
        self.ind = 0            # index of current seg
        self.prev_dur = 0       # duration of previous segs
        self.ended = False

    def value(self, t):
        dt = t - self.prev_dur
        while True:
            seg = self.pft[self.ind]
            if dt < seg.dt - epsilon:
                return seg.val(dt)
            if dt < seg.dt + epsilon and seg.closed_end:
                return seg.y1
            dt -= seg.dt
            self.prev_dur += seg.dt
            self.ind += 1
            if self.ind == len(self.pft):
                self.ended = True
                self.final_value = seg.y1
                return self.final_value
            
# show PFT values with given spacing (for debugging)
def show_pft_vals(pft, dt):
    pft_val = PFTValue(pft)
    t = 0
    last = 0
    while not pft_val.ended:
        v = pft_val.value(t)
        print(t, v, v-last)
        last = v
        t += dt

def show_pft_ints(pft, dt):
    for seg in pft:
        print(seg)
        print('total integral ', seg.integral_total())
        t = 0
        last = 0
        while t<=seg.dt:
            i = seg.integral(t)
            print(t, i, i-last)
            last = i
            t += dt

# ------------------- Dynamics ------------------------

VOL_MULT = 0
VOL_ADD = 1
VOL_SET = 2

# adjust or set volume of selected notes by PFT starting at t0
def vol_adjust_pft(self, pft, t0=0, pred=None, mode=VOL_MULT):
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
        # end time of function
    for n in self.notes:
        if n.time > t_end + epsilon:
            break
        if n.time < t0 - epsilon:
            continue
        if pred and not pred(n):
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
            if v < 0:
                continue
            n.vol *= v
        elif mode == VOL_ADD:
            n.vol += v
        elif mode == VOL_SET:
            if v < 0:
                continue
            n.vol = v/2
        
def vol_adjust(self, v, pred=None, mode=VOL_MULT):
    self.tags_init()
    for n in self.notes:
        if pred and not pred(n):
            continue
        if mode == VOL_MULT:
            n.vol *= v
        elif mode == VOL_ADD:
            n.vol += v
        elif mode == VOL_SET:
            n.vol = v/2
            
def vol_adjust_func(self, func, pred=None, mode=VOL_MULT):
    self.tags_init()
    for n in self.notes:
        if pred and not pred(n):
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
def v_random_uniform(self, min, max, pred=None):
    self.tags_init()
    for note in self.notes:
        if pred and not pred(note): continue
        note.vol *= random.uniform(min, max)

def v_random_normal(self, stddev, max_sigma=2, pred=None):
    self.tags_init()
    for note in self.notes:
        if pred and not pred(note): continue
        while True:
            x = numpy.random.normal()
            if abs(x) < max_sigma: break
        note.vol *= 1+stddev*x

# ------------------- Timing ------------------------

# adjust the timing of selected notes and pedal events.
# pft is a tempo function, which can contain segments (such as Linear)
# and Dirac deltas.
# If bpm is False, its value is performance time per unit score time;
# larger is slower.
# If bpm is True, its value is inverted, so that larger is faster
# (60 = no change, 120 = speed up by 2X)
# In both cases, the value of Dirac deltas is in performance time.
#
# Apply the PFT, starting at score time t0, to the selected notes.
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
def tempo_adjust_pft(
    self, _pft, t0=0, pred=None, normalize=False, bpm=True, debug=False
):
    self.init_all()
    if bpm:
        pft = copy.deepcopy(_pft)
        pft_bpm(pft)    # invert tempo function
    else:
        pft = copy.copy(_pft)

    if debug:
        print('after BPM:')
        print(*pft, sep='\n')
        #print('PFT values:')
        #show_pft_vals(pft, 1/16)
        #print('PFT integrals:')
        #show_pft_ints(pft, 1/16)

    scale_factor = 1
    if normalize:
        scale_factor = 1/pft_avg(pft)
        if debug: print('scale factor: ', scale_factor)

    # append infinite unity segment
    # needed to handle events that lie beyond PFT domain
    pft.append(Unity(9999999))
    
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

    # perf time is score time * 240/tempo
    # so the integral of the PFT is scaled by this.
    # If we want to add a pause (in seconds) to the integral
    # we need to undo this scaling first.
    #
    def dt_to_integral(dt):
        return dt*self.tempo/240
    
    # add the current PFT segment's integral to seg_integral
    # and advance to the next segment
    # 
    def advance_seg():
        nonlocal seg_start, seg_integral, seg_ind, seg, seg_end
        seg_start += seg.dt
        if seg.dt == 0:
            si = dt_to_integral(seg.value)
        else:
            si = seg.integral_total()
        seg_integral += si
        if debug:
            print('    moving to next seg')
        seg_ind += 1
        seg = pft[seg_ind]
        if debug:
            print('    next segment: dt %f integral %f'%(seg.dt, seg.integral_total()))
        seg_end = seg_start + seg.dt

    # the event lies in the current segment.
    # Compute the integral at the event time, and compute its perf time
    #
    def use_seg():
        nonlocal prev_integral, prev_time, prev_perf, prev_perf_adj
        if debug:
            print('    use_seg(): dt', seg.dt)
        if seg.dt == 0:
            si = dt_to_integral(seg.value)
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

        if debug:
            print('event: time %f perf time %f prev_time %f'%(
                event.time, event.perf_time, prev_time)
            )

        # skip if event is not selected
        #
        if pred:
            if event.kind == event_kind_note:
                if not pred(event.obj):
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
                prev_integral = dt_to_integral(seg.value)
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
        # E is at the endpoint of S and the next seg is not a before-Delta
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
                    if debug: print('    next seg not Delta; using and advancing')
                    use_seg()
                    advance_seg()
                    break
                else:
                    if next_seg.after:
                        if debug: print('    next seg is after-Delta: use and advance')
                        use_seg()
                        advance_seg()
                        break
                    if debug: print('    next seg is before-Delta: advance')
            advance_seg()
        if debug:
            print('  Done with event: perf time ', event.perf_time)
    # end loop over events
    self.transfer_start_end_events()

# Note shifting (e.g. for agogic accents)
# shift start time of selected notes by the PFT value
#
def time_shift_pft(self, pft, t0=0, pred=None):
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
        if pred and not pred(n):
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
def sustain(self, t0, t1, pred=None):
    self.time_sort()
    if pred:
        self.tags_init()
    for n in self.notes:
        if n.time<t0 - epsilon:
            continue
        if n.time > t1:
            break
        if pred and not pred(n):
            continue
        end = n.time + n.dur
        if end < t1:
            n.dur = t1 - n.time

# insert a pause of dt before time t.
# If connect is True, extend earlier notes ending at t to preserve legato

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

def pause_before(self, t, dt, connect=True):
    self.init_all()
    pb_aux(self.notes, t, dt, connect)
    pb_aux(self.pedals, t, dt, connect)

# pause after notes at t.
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

def pause_after(self, t, dt):
    self.init_all()
    pa_aux(self.notes, t, dt)
    pa_aux(self.pedals, t, dt)
                
# insert a list of pauses with gaps.
# ts = times when gaps occur
# dts = lengths of gaps
# like a bunch of calls to pause_before(..., connect=False)
# but more efficient because we do one pass through the score.
# Note: tempo_adjust_pft() can insert pauses, but not gaps

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
    pbl_aux(self.notes, ts, dts)
    pbl_aux(self.pedals, ts, dts)

def roll_aux(chord, offsets, is_up):
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
            raise Exception('roll amount exceeds not duration')
        ind += 1

def roll(self, t, offsets, is_up=True, pred=None, verbose=False):
    self.init_all()
    chord = []   # the notes at time t
    for note in self.notes:
        if note.time < t-epsilon:
            continue
        if note.time > t+epsilon:
            break
        if pred and not pred(note): continue
        chord.append(note)
    if chord:
        if verbose:
            print('roll ', offsets, list(map(lambda n: n.pitch, chord)))
        roll_aux(chord, offsets, is_up)

def t_adjust_list(self, offsets, pred):
    self.init_all()
    ind = 0
    for note in self.notes:
        if ind == len(offsets):
            break
        if pred(note):
            note.perf_time += offsets[ind]
            ind += 1

def t_adjust_notes(self, offset, pred):
    self.init_all()
    for note in self.notes:
        if pred(note):
            note.perf_time += offset

def t_adjust_func(self, func, pred):
    self.init_all()
    for note in self.notes:
        if pred(note):
            note.perf_time += func(note)

# perturb start time, and adjust duration to keep end time the same
# Possible TODO: adjust durations of earlier notes that end at this time
#
def t_random_uniform(self, min, max, pred=None):
    self.init_all()
    for note in self.notes:
        if pred and not pred(note):
            continue
        x = random.uniform(min, max)
        note.perf_time += x
        note.perf_dur -= x

def t_random_normal(self, stddev, max_sigma=2, pred=None):
    self.init_all()
    for note in self.notes:
        if pred and not pred(note):
            continue
        while True:
            x = numpy.random.normal()
            if abs(x) < max_sigma:
                break
        y = stddev*x
        note.perf_time += y
        note.perf_dur -= y
                
# --------------- Articulation ----------------------

def score_dur_abs(self, dur, pred=None):
    self.tags_init()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.dur = dur

def score_dur_rel(self, factor, pred=None):
    self.tags_init()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.dur *= factor

def score_dur_func(self, func, pred=None):
    self.tags_init()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.dur = func(note)
            
def perf_dur_abs(self, dur, pred=None):
    self.init_all()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.perf_dur = dur

def perf_dur_rel(self, factor, pred=None):
    self.init_all()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.perf_dur *= factor

def perf_dur_func(self, func, pred=None):
    self.init_all()
    for note in self.notes:
        if pred and not pred(note):
            continue
        note.perf_dur = func(note)

# adjust articulation with a PFT
def perf_dur_pft(self, pft, t0, pred=None, rel=True):
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
        if pred and not pred(n):
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
def vsustain_pft(self, pft, t0=0, pred=None, verbose=False):
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
        if pred and not pred(n):
            continue
        while True:
            if n.time < seg_end - epsilon:
                if seg_end > n.time + n.dur:
                    if seg.level > 0:
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
def pedal_pft(self, pft, t0=0):
    t = t0
    for seg in pft:
        if seg.level > 0:
            self.insert_pedal(PedalUse(t, seg.dt, seg.level, seg.pedal_type))
        t += seg.dt

# ----------- spatialization ----------------

# return array of per-frame stereo positions -1..1,
# based on a PFT defining position as a function of score time.
# If the performance times exceed the PFT,
# use the final PFT value for those frames
def get_pos_array(self, pos_pft, framerate):

    # get the score's note start/end events.
    # Then extract a subset which is strictly monotonic
    # in both score and performance time.
    # This defines a piecewise linear function F
    # mapping perf time to score time.
    # The stereo position at a given frame (perf time t)
    # is the value of pos_pft at score time F(t)
    #
    self.make_start_end_events()
    last_time = 0
    last_perf_time = 0
    events = []
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
    pos_array = [0]*nframes
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
