from MidiFile import MIDIFile

class Note:
    def __init__(self, time, dur, pitch, vol, tags=[]):
        self.time = time
        self.dur = dur
        self.pitch = pitch
        self.vol = vol
        self.tags = tags.copy()
        self.measure_offset = -1
    def print(self):
        t = ''
        if self.measure_offset >= 0:
            t += 'm_off: %.4f '%self.measure_offset
        t += ' '.join(self.tags)
        print('t: %.4f d: %.4f perf_t: %.4f perf_d: %.4f pitch: %d vol: %.4f chord: (%d/%d) %s'%(
            self.time, self.dur, self.perf_time, self.perf_dur, self.pitch, self.vol,
            self.chord_pos, self.nchord, t
        ))

class Pedal:
    def __init__(self, time, dur, level=1, sostenuto=False):
        self.time = time
        self.dur = dur
        self.level = level
        self.sostenuto = False
        
epsilon = 1e-4    # slop factor for time in case of round-off

class NoteSet:
    def __init__(self):
        self.notes = []
        self.cur_time = 0
        self.tempo = 60    # beats per minute
        self.measures = []
        self.pedals = []
        self.done_called = False
        
    def insert_note(self, note):
        self. notes.append(note)
    def append_note(self, note):
        note.time = self.cur_time
        self.notes.append(note)
    def advance_time(self, dur):
        self.cur_time += dur

    def insert_ns(self, t, ns):
        for note in ns.notes:
            note.time += t
            self.insert_note(note)

    def append_ns(self, nss):
        longest = 0
        for ns in nss:
            if ns.cur_time > longest: longest = ns.cur_time
            self.insert_ns(self.cur_time, ns)
        self.cur_time += longest
            
    def insert_measure(self, t):
        self.measures.append(t)

    def insert_pedal(self, pedal):
        self.pedals.append(pedal)
        
    def print(self):
        if not self.done_called:
            raise Exception('Call done() before print()')
        m_ind = 0
        for note in self.notes:
            if m_ind < len(self.measures):
                if note.time > self.measures[m_ind] - epsilon:
                    print('measure %d'%m_ind);
                    m_ind += 1
            note.print()
            
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
                        print('warning: 2 notes at time %f have same pitch %d'%(
                            cnote.time, cnote.pitch
                        ))
            else:
                cnote = chord[0]
                cnote.nchord = 1
                cnote.chord_pos = 0
                
        for note in self.notes:
            note.perf_time = note.time*4*60/ self.tempo
            note.perf_dur = note.dur*4*60/self.tempo
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
            pedal.perf_time = pedal.time*4*60/self.tempo
            pedal.perf_dur = pedal.dur*4*60/self.tempo
                
        # initialize for nuance stuff
        #
        self.measure_offsets()
        self.flag_outer()
        self.vol_cur_time = 0
        self.vol_ind = 0
        self.timing_init()
        
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
                    # print("simultaneous overlap at time %f"%(note.perf_time))
                    # simultaneous -  earlier note subsumes later one
                    #
                    n2.vol = max(n2.vol, note.vol)
                    md = max(n2.perf_dur, note.perf_dur)
                    nd.perf_dur = md
                    end_time[note.pitch] = note.perf_time+md
                else:
                    #print("overlap at times %f %f"%(n2.perf_time, note.perf_time))
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

     # make an auxiliary structure with start/end events
    #
    def timing_init(self):
        self.start_end = []
        for note in self.notes:
            self.start_end.append(Event(note.time, note, event_kind_note, True))
            self.start_end.append(Event(note.time+note.dur, note, event_kind_note, False))
        for pedal in self.pedals:
            self.start_end.append(Event(pedal.time, pedal, event_kind_pedal, True))
            self.start_end.append(Event(pedal.time+pedal.dur, pedal, event_kind_pedal, False))
        self.start_end.sort(key=lambda x: x.time)
        self.cur_ind = 0    # index into ns.start_end
        self.cur_time = 0
        self.cur_perf_time = 0
        
    # compute offsets from measure boundaries
    #
    def measure_offsets(self):
        if not self.measures: return
        m_ind = 0
        m_time = -9999
        for note in self.notes:
            if m_ind < len(self.measures):
                if note.time > self.measures[m_ind] - epsilon:
                    m_time = self.measures[m_ind]
                    m_ind += 1
            note.measure_offset = note.time - m_time

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
            
 # represents the start or end of a note or pedal application
#
event_kind_note = 0
event_kind_pedal = 1
class Event:
    def __init__(self, time, obj, kind, is_start):
        self.time = time
        self.obj = obj
        self.kind = kind
        self.is_start = is_start
        
def test():
    y = NoteSet()
    y.add(Note(1,2,3,4))
    y.add(Note(0,2,3,4))
    y.sort_time()
    y.remove_overlap()
    y.print()
