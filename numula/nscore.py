# classes for notes and scores
# see https://github.com/davidpanderson/Numula/wiki/Scores

import numula.MidiFile
from numula.constants import *
from typing import Callable

class Note:
    def __init__(self,
        time: float,
        dur: float,
        pitch: int,
        vol: float,
        tags: list[str] = []
    ):
        if pitch < 0 or pitch > 127:
            raise Exception('illegal pitch %d at time %f'%(pitch, time))
        self.time = time
        self.dur = dur
        self.pitch = pitch
        self.vol = vol
        self.tags = tags.copy()
        self.measure_type = None
        self.measure_offset = -1
        self.perf_time: float = 0.
        self.perf_dur: float = 0.
        self.chord_pos = 0
        self.nchord = 0

    def __str__(self):
        t = ''
        if self.measure_type:
            t += 'm_off: %.4f %s '%(self.measure_offset, self.measure_type)
        t += ','.join(self.tags)
        return 't: %.4f d: %.4f perf_t: %.4f perf_d: %.4f pitch: %s vol: %.4f %s'%(
            self.time, self.dur, self.perf_time, self.perf_dur,
            pitch_name(self.pitch), self.vol,
            t
        )

# type for a note selector function
#
type Selector = Callable[[Note], bool] | None

# some nuance functions take a function mapping Notes to floating point values
# (e.g. durations or volumes)
#
type NoteToFloat = Callable[[Note], float]

pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def pitch_name(n: int):
    return '%s%d'%(pitch_names[n%12], n//12)

# this is used both as
# - a PFT primitive
# - an element of ScoreBasic.pedals
#   (in which case time, perf_time, perf_dur, and pedal_type are defined)
#
class PedalSeg:
    def __init__(self,
        dur: float,
        level0: float=1,
        level1: float=1,
        closed_start: bool=True,
        closed_end: bool=True,
        time: float=0,
        type: int=PEDAL_SUSTAIN
    ):
        self.dur = dur
        self.dt = dur
        self.level0 = level0
        self.level1 = level1
        self.closed_start = closed_start
        self.closed_end = closed_end
        self.time = time
        self.pedal_type = type
        self.perf_time = 0.
        self.perf_dur = 0.

    def __str__(self):
        return 'pedal time %.4f dur %.4f perf_time %.4f perf_dur %.4f type %d levels %f %f closed %s %s'%(
            self.time, self.dt, self.perf_time, self.perf_dur,
            self.pedal_type, self.level0, self.level1,
            'yes' if self.closed_start else 'no',
            'yes' if self.closed_end else 'no'
        )
    
class Measure:
    def __init__(self, time: float, dur: float, type: str):
        self.time = time
        self.dur = dur
        self.type = type

    def __str__(self):
        return 'measure: %.4f-%.4f'%(self.time, self.time+self.dur)
        
event_kind_note = 0
event_kind_pedal = 1

# basic score class
# nuance functions are added in Score (inherited)
#
class ScoreBasic:
    def __init__(self,
        tempo: float = 60,
        verbose = False
    ):
        self.notes: list[Note] = []
        self.cur_time = 0.
        self.tempo = tempo    # beats per minute
        self.verbose = verbose
        self.measures: list[Measure] = []
        self.pedals: list[PedalSeg] = []
        self.done_called = False
        self.m_cur_time = 0.    # for appending measures
        self.clear_flags()

    def __str__(self):
        self.init_all()     # sort, set perf times, set tags
        m_ind = 0
        pedal_ind = 0
        x = ''
        for note in self.notes:
            if m_ind < len(self.measures):
                m = self.measures[m_ind]
                if note.time > m.time - epsilon:
                    x += str(m) + '\n'
                    m_ind += 1
            if pedal_ind < len(self.pedals):
                p = self.pedals[pedal_ind]
                if note.time > p.time - epsilon:
                    x += str(p) + '\n'
                    pedal_ind += 1
            x += str(note) + '\n'
        return x
        
    def insert_note(self, note:Note):
        self.notes.append(note)
        self.clear_flags()

    def append_note(self, note:Note):
        note.time = self.cur_time
        self.notes.append(note)
        self.clear_flags()

    def advance_time(self, dur:float):
        self.cur_time += dur

    # Merge a Score into this one, starting at time t,
    # optionally tagging the notes.
    # This doesn't copy anything, and the notes and pedals are modified.
    # to insert a Score more than once, do a deep copy on it
    #
    def insert_score(self, score:'ScoreBasic', t:float=0, tag:str=''):
        for note in score.notes:
            note.time += t
            if tag:
                note.tags.append(tag)
            self.insert_note(note)
        for pedal in score.pedals:
            pedal.time += t
            self.insert_pedal(pedal)
        for measure in score.measures:
            measure.time += t
            self.insert_measure(measure)
        self.clear_flags()
        return self

    # append a score to this one
    #
    def append_score(self, score:'ScoreBasic', tag:str=''):
        self.insert_score(score, self.cur_time, tag)
        self.cur_time += score.cur_time
        self.clear_flags()
        return self

    # append a list of scores in parallel
    #
    def append_scores(self, scores:list['ScoreBasic'], tag:str=''):
        longest = 0.
        for score in scores:
            longest = max(longest, score.cur_time)
            self.insert_score(score, self.cur_time, tag)
        self.cur_time += longest
        self.clear_flags()
        return self

            
    def insert_measure(self, m:Measure):
        self.measures.append(m)
        self.clear_flags()
        return self
        
    def append_measure(self, dur:float, mtype:str):
        m = Measure(self.m_cur_time, dur, mtype)
        self.measures.append(m)
        self.m_cur_time += dur
        self.clear_flags()
        return self

    def insert_pedal(
        self,
        pedal: PedalSeg,
        type: int = None,
        time: float = None
    ):
        if time is not None:
            pedal.time = time
        if type is None:
            pedal.type = PEDAL_SUSTAIN
        self.pedals.append(pedal)
        self.clear_flags()
        return self

    def tag(self, tag:str):
        for note in self.notes:
            note.tags.append(tag)
        return self
        
    # convert score time to real time, given tempo
    def score_to_perf(self, t:float):
        return t*4*60/self.tempo

    def time_sort(self):
        if self.time_sorted:
            return
        if self.verbose:
            print('sorting notes, pedals and measures')
        self.time_sorted = True
        self.notes.sort(key=lambda x: x.time)
        self.pedals.sort(key=lambda x: x.time)
        self.measures.sort(key=lambda x: x.time)

    def time_sort_clear(self):
        self.time_sorted = False

    # initialize perf times if not already done
    #
    def perf_init(self):
        if self.verbose: print('initializing performance times')
        if self.perf_inited:
            if self.verbose: print('already inited')
            return
        self.perf_inited = True
        if not self.notes:
            raise Exception('no notes')
        if len(self.notes) != len(set(self.notes)):
            raise Exception('self.notes has dups!!')
        # set perf time and dur in such a way that playback will be at the
        # tempo given by self.tempo.
        #
        for note in self.notes:
            note.perf_time = self.score_to_perf(note.time)
            note.perf_dur = self.score_to_perf(note.dur)
        for pedal in self.pedals:
            pedal.perf_time = self.score_to_perf(pedal.time)
            pedal.perf_dur = self.score_to_perf(pedal.dur)

    def perf_init_clear(self):
        if self.verbose: print('perf_init_clear()')
        self.perf_inited = False
        
    def tags_init(self):
        if self.tags_inited:
            return True
        if self.verbose:
            print('initializing note tags')
        self.tags_inited = True
        chord = []
        def do_chord(chord):
            n = len(chord)
            if n > 1:
                chord.sort(key=lambda x: x.pitch)
                for i in range(n):
                    cnote = chord[i]
                    cnote.nchord = n
                    cnote.chord_pos = i
                    if i>1 and cnote.pitch == chord[i-1].pitch:
                        print('warning: 2 notes at time %f have same pitch %s'%(
                            cnote.time, pitch_name(cnote.pitch)
                        ))
            else:
                cnote = chord[0]
                cnote.nchord = 1
                cnote.chord_pos = 0
                
        for note in self.notes:
            if chord:
                if note.time > chord_time + epsilon:
                    do_chord(chord)
                    chord = []
                    if 'ch' in note.tags:
                        chord = [note]
                        chord_time = note.time
                else:
                    if 'ch' in note.tags:
                        chord.append(note)
            else:
                if 'ch' in note.tags:
                    chord = [note]
                    chord_time = note.time
        if chord:
            do_chord(chord)

        self.measure_offsets()
        self.flag_outer()

    def tags_init_clear(self):
        self.tags_inited = False

    def clear_flags(self):
        self.time_sorted = False
        self.perf_inited = False
        self.tags_inited = False

    def init_all(self):
        if self.verbose: print('init_all()')
        self.time_sort()
        self.perf_init()
        self.tags_init()

    # shift perf times to start at time t >= 0
    # in particular, avoid negative times; MIDI files don't like them
    #
    def shift_start(self, t: float):
        self.notes.sort(key=lambda x: x.perf_time)
        t0 = self.notes[0].perf_time
        dt = t - t0
        if dt == 0:
            return
        for note in self.notes:
            note.perf_time += dt
        for pedal in self.pedals:
            pedal.perf_time += dt

    # get the max performance end time
    # Note: the .wav file produced by pianoteq
    # will be a second or two longer than this
    def perf_end_time(self):
        self.make_perf_shift_start(1)
        x = 0
        for n in self.notes:
            t = n.perf_time + n.perf_dur
            if t>x: x = t
        for p in self.pedals:
            t = p.perf_time + p.perf_dur
            if t>x: x = t
        return x

    # write selected notes to MIDI file
    def write_midi(self,
        filename: str, selector: Selector=None, verbose: bool = False
    ):
        self.init_all()
        self.shift_start(1)
        vstr = ''

        # MIDIutils doesn't handle overlapping notes correctly,
        # so adjust note times to remove overlap
        #
        self.remove_overlap(verbose)

        f = numula.MidiFile.MIDIFile(deinterleave=False)
        f.addTempo(0, 0, 60)
        for note in self.notes:
            if selector and not selector(note):
                continue
            if note.vol > 1:
                print('%s at time %f has vol %f > 1; setting to 1'%(
                    pitch_name(note.pitch), note.time, note.vol
                ))
            v = int(note.vol * 128)
            if v < 2: v = 2
            if v > 127: v = 127
            if verbose:
                vstr += 'MIDI note: pitch %d start %f end %f vol %f\n'%(
                    note.pitch, note.perf_time,
                    note.perf_time + note.perf_dur, v
                )
            f.addNote(0, 0, note.pitch, note.perf_time, note.perf_dur, v)
        if self.pedals:
            self.adjust_pedal_times()
            self.write_midi_pedals(f)

        with open(filename, "wb") as file:
            f.writeFile(file)
        if verbose:
            print(vstr)

    # generate MIDI events for pedals
    #
    def write_midi_pedals(self, f):
        soft = []
        sost = []
        sustain = []
        for pedal in self.pedals:
            if pedal.pedal_type == PEDAL_SOFT:
                soft.append(pedal)
            elif pedal.pedal_type == PEDAL_SOSTENUTO:
                sost.append(pedal)
            elif pedal.pedal_type == PEDAL_SUSTAIN:
                sustain.append(pedal)
        self.write_midi_pedals_type(f, soft, PEDAL_SOFT)
        self.write_midi_pedals_type(f, sost, PEDAL_SOSTENUTO)
        self.write_midi_pedals_type(f, sustain, PEDAL_SUSTAIN)

    def write_midi_pedals_type(self, f, pedals, type):
        # set P.have_next if there's a segment immediately following P
        prev = None
        for pedal in pedals:
            pedal.have_next = False
            if prev:
                if abs(p.perf_time+p.perf_dur - pedal.perf_time) < epsilon:
                    prev.have_next = True
        for pedal in pedals:
            t0 = pedal.perf_time
            t1 = pedal.perf_time + pedal.perf_dur
            if pedal.closed_start:
                t0 -= epsilon
            else:
                t0 += epsilon
            level0 = int(64+pedal.level0*63)
            level1 = int(64+pedal.level1*63)
            if level0 == level1:
                f.addControllerEvent(0, 0, t0, type, level0)
            else:
                # e.g. if levels differ by 1, 2nd should go halfway in time
                diff = level1 - level0
                step = 1 if diff>0 else -1
                n = abs(diff)
                dt = t1 - t0
                for i in range(n):
                    level = level0 + i*step
                    t = t0 + (i*dt)/n
                    f.addControllerEvent(0, 0, t, type, level)
            if pedal.have_next:
                if not pedal.closed_end:
                    f.addControllerEvent(0, 0, t1-2*epsilon, type, 0)
            else:
                if pedal.closed_end:
                    f.addControllerEvent(0, 0, t1+epsilon, type, 0)
                else:
                    f.addControllerEvent(0, 0, t1-epsilon, type, 0)
        
    # ----- implementation ----

    # if a note starts while one of the same pitch is sounding,
    # truncate the first note.
    # MIDIUtil doesn't handle this case correctly -
    # you end up with stuck notes.
    #
    def remove_overlap(self, verbose=False):
        end_time = [-1]*128
        cur_note = [None]*128
        out = []
        vstr = ''
        midi_eps = .05
            # make sure MIDI events on a given pitch are separated by this
            # Originally this was .001.
            # But it turns out that with Pianoteq, if a note is playing loud,
            # that loudness will bleed into a subsequent soft note
            # unless the two are separated by something like this.
        for note in self.notes:
            if note.perf_time < end_time[note.pitch]+midi_eps:
                # note start while a note of this pitch is already sounding
                n2 = cur_note[note.pitch]
                if note.perf_time - n2.perf_time < epsilon:
                    vstr += "simultaneous start overlap on %s at time %f\n"%(
                        pitch_name(note.pitch), note.perf_time
                    )
                    # simultaneous start - combine notes
                    # by modifying first note (already in out) in place
                    # Set vol and duration to the max of the two.
                    #
                    n2.vol = max(n2.vol, note.vol)
                    md = max(n2.perf_dur, note.perf_dur)
                    n2.perf_dur = md
                    end_time[note.pitch] = note.perf_time+md
                else:
                    if verbose and note.perf_time < end_time[note.pitch] + midi_eps:
                        # show warning if overlap is nontrivial
                        vstr += "overlap on %s:\n"%(pitch_name(note.pitch))
                        vstr += str(n2)+'\n'
                        vstr += str(note)+'\n'
                   # end earlier note early
                    n2.perf_dur = (note.perf_time - n2.perf_time) - midi_eps
                    out.append(note)
                    end_time[note.pitch] = note.perf_time+note.perf_dur
                    cur_note[note.pitch] = note
            else:
                out.append(note)
                end_time[note.pitch] = note.perf_time+note.perf_dur
                cur_note[note.pitch] = note
        self.notes = out
        if verbose:
            print(vstr)

     # make a sorted list of start/end events
    #
    def make_start_end_events(self):
        self.start_end: list[Event] = []
        for note in self.notes:
            self.start_end.append(Event(note, event_kind_note, True))
            self.start_end.append(Event(note, event_kind_note, False))
        for pedal in self.pedals:
            self.start_end.append(Event(pedal, event_kind_pedal, True))
            self.start_end.append(Event(pedal, event_kind_pedal, False))
        self.start_end.sort(key=lambda x: x.time)

    # transfer perf times from start/end events back to Note and PedalSeg
    #
    def transfer_start_end_events(self):
        for event in self.start_end:
            obj = event.obj
            if event.is_start:
                obj.perf_time = event.perf_time
            else:
                obj.perf_dur = event.perf_time - obj.perf_time
                
    def print_start_end_events(self):          
        for event in self.start_end:
            print('is_start', event.is_start, ' perf_time', event.perf_time)
            
    # for notes that lie in measures,
    # compute the offset and tag the note with the measure type
    #
    def measure_offsets(self):
        self.time_sort()
        if not self.measures:
            return
        m_ind = 0
        m_time = -9999
        for note in self.notes:
            # skip measures that end before this note
            while m_ind < len(self.measures):
                m = self.measures[m_ind]
                if note.time > m.time + m.dur - epsilon:
                    m_ind += 1
                else:
                    break
            if m_ind < len(self.measures):
                if m.time < note.time + epsilon:
                    note.measure_type = m.type
                    note.measure_offset = note.time - m.time
            if not note.measure_type:
                raise Exception('note is not in any measure')

    # tag notes that are the highest or lowest sounding notes at their start
    #
    @staticmethod
    def flag_outer_aux(active: list[Note], starting: list[Note]):
        #print('flag_aux: %d active, %d starting'%(len(active), len(starting)))
        min = 128
        max = -1
        for n in active:
            if n.pitch < min: min = n.pitch
            if n.pitch > max: max = n.pitch
        for n in starting:
            if n.pitch == max:
                n.tags.append('top')
            if n.pitch == min:
                n.tags.append('bottom')
            
    def flag_outer(self):
        cur_time = 0
        active = []     # notes active at current time
        starting = []    # notes that started at current time
        for note in self.notes:
            if note.time > cur_time + epsilon:
                if len(starting):
                    ScoreBasic.flag_outer_aux(active, starting)
                cur_time = note.time
                new_active = [note]
                for n in active:
                    if n.time + n.dur > cur_time + epsilon:
                        new_active.append(n)
                active = new_active
                starting = [note]
            else:
                active.append(note)
                starting.append(note)
        ScoreBasic.flag_outer_aux(active, starting)

    # Adjust performance time of pedal events so that they do the right thing
    # even if note start times have been adjusted.
    # Sustain pedal:
    # start time is the min of the start times
    # of notes with score times in the pedal interal;
    # we need to "catch" all these notes, even if they got moved earlier
    # Sostenuto pedal:
    # if a note is active (in score time) at the pedal start,
    # but its perf time is greater than pedal perf start,
    # set pedal perf to that time
    # plus an epsilon so that the pedal "catches" all those notes
    #
    def adjust_pedal_times(self):
        self.time_sort()
        ped_ind = 0
        cur_ped = self.pedals[0]
        for note in self.notes:
            if ped_ind == len(self.pedals):
                break
            if cur_ped.pedal_type == PEDAL_SOSTENUTO:
                if note.time + note.dur < cur_ped.time - epsilon:
                    continue
                if note.time > cur_ped.time + epsilon:
                    ped_ind += 1
                else:
                    if note.perf_time > cur_ped.perf_time:
                        cur_ped.perf_time = note.perf_time + epsilon
            else:
                # sustain, soft
                if note.time < cur_ped.time:
                    continue
                if note.time > cur_ped.time + cur_ped.dur:
                    ped_ind += 1
                else:
                    if note.perf_time < cur_ped.perf_time:
                        cur_ped.perf_time = note.perf_time
        #for pedal in self.pedals:
            # don't want pedal down during attack of notes right at end.
            # On Pianoteq this can cause stuck notes (possibly a bug)
            #pedal.perf_dur -= .01

    # trim to times t0..t1
    #
    def trim(self, t0: float, t1: float):
        new_notes = []
        for note in self.notes:
            if note.time < t0-epsilon:
                continue
            if note.time > t1-epsilon:
                continue
            new_notes.append(note)
        self.notes = new_notes
        new_pedals: list[PedalSeg] = []
        for ped in self.pedals:
            if ped.time < t0-epsilon:
                continue
            if ped.time > t1-epsilon:
                continue
            new_pedals.append(ped)
        self.pedals = new_pedals

    # change note durations based on pattern
    #
    def dur_pattern(self, durs: list[float], t0: float, t1: float):
        n = len(durs)
        i = 0
        for note in self.notes:
            if note.time > t1 - epsilon:
                break
            if note.time < t0 - epsilon:
                continue
            note.dur = durs[i]
            i += 1
            if i == n:
                i = 0

    # scale volumes to given range
    #
    def vol_scale(self, v0: float, v1: float):
        d = v1 - v0
        for note in self.notes:
            note.vol = v0 + note.vol*d
            
# end of Score

# represents the start or end of a note or pedal application
#
class Event:
    def __init__(self, obj, kind, is_start):
        if is_start:
            self.time = obj.time
            self.perf_time = obj.perf_time
        else:
            self.time = obj.time + obj.dur
            self.perf_time = obj.perf_time + obj.perf_dur
        self.obj = obj
        self.kind = kind
        self.is_start = is_start
