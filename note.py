# This file is part of Numula
# Copyright (C) 2022 David P. Anderson
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

# classes for notes and sets of notes

from MidiFile import MIDIFile

class Note:
    def __init__(self, time, dur, pitch, vol, tags=[]):
        self.time = time
        self.dur = dur
        self.pitch = pitch
        self.vol = vol
        self.tags = tags.copy()
        self.measure_type = None
        self.measure_offset = -1
        self.perf_time = 0
        self.perf_dur = 0
        self.chord_pos = 0
        self.nchord = 0
    def print(self):
        t = ''
        if self.measure_type:
            t += 'm_off: %.4f %s '%(self.measure_offset, self.measure_type)
        t += ' '.join(self.tags)
        print('t: %.4f d: %.4f perf_t: %.4f perf_d: %.4f pitch: %s vol: %.4f chord: (%d/%d) %s'%(
            self.time, self.dur, self.perf_time, self.perf_dur,
            pitch_name(self.pitch), self.vol,
            self.chord_pos, self.nchord, t
        ))

pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def pitch_name(n):
    return '%s%d'%(pitch_names[n%12], n//12)
    
class Pedal:
    def __init__(self, time, dur, level=1, sostenuto=False):
        self.time = time
        self.dur = dur
        self.level = level
        self.sostenuto = False

class Measure:
    def __init__(self, time, dur, type):
        self.time = time
        self.dur = dur
        self.type = type
        
epsilon = 1e-5    # slop factor for time in case of round-off
event_kind_note = 0
event_kind_pedal = 1

class NoteSet:
    def __init__(self, nss=[]):
        self.notes = []
        self.cur_time = 0
        self.tempo = 60    # beats per minute
        self.measures = []
        self.pedals = []
        self.done_called = False
        self.m_cur_time = 0    # for appending measures
        self.append_ns(nss)
        
    def insert_note(self, note):
        self.notes.append(note)
    def append_note(self, note):
        note.time = self.cur_time
        self.notes.append(note)
    def advance_time(self, dur):
        self.cur_time += dur

    def insert_ns(self, t, ns, tag=None):
        for note in ns.notes:
            note.time += t
            if tag:
                note.tags.append(tag)
            self.insert_note(note)

    def append_ns(self, nss, tag=None):
        longest = 0
        for ns in nss:
            longest = max(longest, ns.cur_time)
            self.insert_ns(self.cur_time, ns, tag)
        self.cur_time += longest
            
    def insert_measure(self, m):
        self.measures.append(m)
        
    def append_measure(self, dur, type):
        m = Measure(self.m_cur_time, dur, type)
        self.measures.append(m)
        self.m_cur_time += dur

    def insert_pedal(self, pedal):
        self.pedals.append(pedal)
        
    def print(self):
        if not self.done_called:
            raise Exception('Call done() before print()')
        m_ind = 0
        for note in self.notes:
            if m_ind < len(self.measures):
                m = self.measures[m_ind]
                if note.time > m.time - epsilon:
                    print('measure %d: %.4f-%.4f'%(m_ind+1, m.time, m.time+m.dur));
                    m_ind += 1
            note.print()

    # convert score time to real time, assuming quarter=60
    def score_to_perf(self, t):
        return t*4*60/self.tempo
    
    def done(self):
        if not self.notes:
            raise Exception('no notes')
        self.done_called = True
        self.notes.sort(key=lambda x: x.time)
        # set perf time and dur in such a way that playback will be at the
        # tempo given by self.tempo.
        # These will be modified if you use nuance functions.
        #
        # Also set note.nchord and not.chord_pos
        #
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
            note.perf_time = self.score_to_perf(note.time)
            note.perf_dur = self.score_to_perf(note.dur)
            if chord:
                if note.time > chord_time + epsilon:
                    do_chord(chord)
                    chord = [note]
                    chord_time = note.time
                else:
                    chord.append(note)
            else:
                chord = [note]
                chord_time = note.time
        do_chord(chord)

        for pedal in self.pedals:
            pedal.perf_time = self.score_to_perf(pedal.time)
            pedal.perf_dur = self.score_to_perf(pedal.dur)
                
        # initialize for nuance stuff
        #
        self.measure_offsets()
        self.flag_outer()
                
    def write_midi(self, filename):
        if not self.done_called:
            raise Exception('Call done() before write_midi()')

        # shift to avoid negative times; MIDI files don't like them
        #
        self.notes.sort(key=lambda x: x.perf_time)
        t0 = self.notes[0].perf_time
        if t0 < 0:
            for note in self.notes:
                note.perf_time -= t0
            for pedal in self.pedals:
                pedal.perf_time -= t0

        # MIDIutils doesn't handle overlapping notes correctly, so remove them
        #
        self.remove_overlap()

        f = MIDIFile(deinterleave=False)
        f.addTempo(0, 0, 60)
        for note in self.notes:
            if note.vol > 1:
                print('%s at time %f has vol %f; setting to 1'%(
                    pitch_name(note.pitch), note.time, note.vol
                ))
            v = int(note.vol * 128)
            if v < 2: v = 2
            if v > 127: v = 127
            f.addNote(0, 0, note.pitch, note.perf_time, note.perf_dur, v)
        if self.pedals:
            self.adjust_pedal_times()
            for pedal in self.pedals:
                c = 66 if pedal.sostenuto else 64
                level = int(64+pedal.level*63)
                f.addControllerEvent(0, 0, pedal.perf_time, c, level)
                f.addControllerEvent(0, 0, pedal.perf_time + pedal.perf_dur, c, 0)
        with open(filename, "wb") as file:
            f.writeFile(file)

    def set_tempo(self, tempo):
        if  self.done_called:
            raise Exception('Call set_tempo() before done()')
        self.tempo = tempo

    # ----- implementation ----

    # if a note starts while one of the same pitch is sounding,
    # truncate the first note.
    # MIDIUtil doesn't handle this case correctly -
    # you end up with stuck notes.
    #
    def remove_overlap(self):
        end_time = [0]*128
        cur_note = [None]*128
        out = []
        for note in self.notes:
            if note.perf_time < end_time[note.pitch]:
                # note of this pitch is already sounding
                n2 = cur_note[note.pitch]
                if n2.perf_time > note.perf_time - epsilon:
                    print("simultaneous overlap on %s at time %f"%(
                        pitch_name(note.pitch), note.perf_time
                    ))
                    # simultaneous -  earlier note subsumes later one
                    #
                    n2.vol = max(n2.vol, note.vol)
                    md = max(n2.perf_dur, note.perf_dur)
                    n2.perf_dur = md
                    end_time[note.pitch] = note.perf_time+md
                else:
                    print("overlap on %s: notes at %f and %f"%(
                        pitch_name(note.pitch), n2.perf_time, note.perf_time
                    ))
                    # end earlier note early
                    n2.perf_dur = (note.perf_time - n2.perf_time) - epsilon
                    out.append(note)
                    end_time[note.pitch] = note.perf_time+note.perf_dur
                    cur_note[note.pitch] = note
            else:
                out.append(note)
                end_time[note.pitch] = note.perf_time+note.perf_dur
                cur_note[note.pitch] = note
        self.notes = out

     # make a sorted list of start/end events
    #
    def make_start_end_events(self):
        self.start_end = []
        for note in self.notes:
            self.start_end.append(Event(note, event_kind_note, True))
            self.start_end.append(Event(note, event_kind_note, False))
        for pedal in self.pedals:
            self.start_end.append(Event(pedal, event_kind_pedal, True))
            self.start_end.append(Event(pedal, event_kind_pedal, False))
        self.start_end.sort(key=lambda x: x.time)
        self.cur_ind = 0    # index into ns.start_end
        self.cur_time = 0
        self.cur_perf_time = 0

    # transfer perf times from start/end events back to Note and Pedal
    #
    def transfer_start_end_events(self):
        for event in self.start_end:
            obj = event.obj
            if event.is_start:
                obj.perf_time = event.perf_time
            else:
                obj.perf_dur = event.perf_time - obj.perf_time
                
    # for notes that lie in measures,
    # compute the offset and tag the note with the measure type
    #
    def measure_offsets(self):
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
    def flag_outer_aux(active, started):
        #print('flag_aux: %d active, %d started'%(len(active), len(started)))
        min = 128
        max = -1
        for n in active:
            if n.pitch < min: min = n.pitch
            if n.pitch > max: max = n.pitch
        for n in started:
            if n.pitch == max:
                n.tags.append('top')
            if n.pitch == min:
                n.tags.append('bottom')
            
    def flag_outer(self):
        cur_time = 0
        active = []     # notes active at current time
        started = []    # notes that started at current time
        for note in self.notes:
            if note.time > cur_time + epsilon:
                if len(started):
                    NoteSet.flag_outer_aux(active, started)
                cur_time = note.time
                new_active = [note]
                for n in active:
                    if n.time + n.dur > cur_time + epsilon:
                        new_active.append(n)
                active = new_active
                started = [note]
            else:
                active.append(note)
                started.append(note)
        NoteSet.flag_outer_aux(active, started)

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
        # need to scan notes by score time
        notes2 = list(self.notes)
        notes2.sort(key=lambda x: x.time)
        self.pedals.sort(key=lambda x: x.time)
        ped_ind = 0
        cur_ped = self.pedals[0]
        for note in notes2:
            if ped_ind == len(self.pedals):
                break
            if cur_ped.sostenuto:
                if note.time + note.dur < cur_ped.time - epsilon:
                    continue
                if note.time > cur_ped.time + epsilon:
                    ped_ind += 1
                else:
                    if note.perf_time > cur_ped.perf_time:
                        cur_ped.perf_time = note.perf_time + epsilon
            else:
                # sustain
                if note.time < cur_ped.time:
                    continue
                if note.time > cur_ped.time + cur_ped.dur:
                    ped_ind += 1
                else:
                    if note.perf_time < cur_ped.perf_time:
                        cur_ped.perf_time = note.perf_time
                        
    from nuance import vol_adjust_pft, vol_adjust, vol_adjust_func
    from nuance import tempo_adjust_pft, sustain, pause_before, pause_after
    from nuance import roll, t_adjust_list, t_adjust_notes, t_adjust_func
    from nuance import t_random_uniform, t_random_normal
    from nuance import score_dur_abs, score_dur_rel, score_dur_func
    from nuance import perf_dur_abs, perf_dur_rel, perf_dur_func
    
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
