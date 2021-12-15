from midiutil import MIDIFile

class Note:
    def __init__(self, time, dur, pitch, vol, tags=[]):
        self.time = time
        self.dur = dur
        self.pitch = pitch
        self.vol = vol
        self.tags = tags
    def print(self):
        t = ' '.join(self.tags)
        print('time: %f dur: %f pitch: %d vol: %f%s'%(
            self.perf_time, self.perf_dur, self.pitch, self.vol, t
        ))

epsilon = 1e-4    # slop factor for time in case of round-off

class NoteSet:
    def __init__(self):
        self.notes = []
        self.cur_time = 0
        self.tempo = 60    # beats per minute
    def add(self, note):
        note.perf_time = note.time*4*60/ self.tempo
        note.perf_dur = note.dur*4*60/self.tempo
        self. notes.append(note)
    def print(self):
        for note in self.notes:
            note.print()
    def sort_time(self):
        self.notes.sort(key=lambda x: x.time)
    def write_midi(self, filename):
        f = MIDIFile(1)
        f.addTempo(0, 0, 60)
        for note in self.notes:
            v = int(note.vol * 128)
            if v < 2: v = 2
            if v > 127: v = 127
            f.addNote(0, 0, note.pitch, note.perf_time, note.perf_dur, v)
        with open(filename, "wb") as file:
            f.writeFile(file)
    def add_list(self, time, new_notes):
        for note in new_notes:
            note.time += time
            self.add(note)

    # remove notes that start while a note of the same pitch is active
    # Useful for cleaning up randomly-generated stuff
    #
    def remove_overlap(self):
        self.sort_time()
        end_time = [0]*128
        out = []
        for note in self.notes:
            if note.time < end_time[note.pitch]:
                continue
            out.append(note)
            end_time[note.pitch] = note.time+note.dur
        self.notes = out
        
def test():
    y = NoteSet()
    y.add(Note(1,2,3,4))
    y.add(Note(0,2,3,4))
    y.sort_time()
    y.remove_overlap()
    y.print()
