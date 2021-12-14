from midiutil import MIDIFile

class Note:
    def __init__(self, time, dur, pitch, vol):
        self.time = time
        self.dur = dur
        self.pitch = pitch
        self.vol = vol
        self.highest = False
        self.lowest = False
    def print(self):
        h = " highest" if self.highest else ''
        l = ' lowest' if self.lowest else ''
        print('time: %f dur: %f pitch: %d vol: %d%s%s'%(
            self.time, self.dur, self.pitch, self.vol, l, h
        ))

epsilon = 1e-4    # slop factor for time in case of round-off

class NoteSet:
    def __init__(self):
        self.notes = []
        self.cur_time = 0
    def add(self, note):
        self. notes.append(note)
    def print(self):
        for note in self.notes:
            note.print()
    def sort_time(self):
        self.notes.sort(key=lambda x: x.time)
    def write_midi(self, tempo, filename):
        f = MIDIFile(1)
        f.addTempo(0, 0, tempo/4)
        for note in self.notes:
            f.addNote(0, 0, note.pitch, note.time, note.dur, note.vol)
        with open(filename, "wb") as file:
            f.writeFile(file)
    def append(self, new_notes):
        for note in new_notes:
            note.time += self.cur_time
            self.add(note)
    def insert(self, time, new_notes):
        self.cur_time = time
        self.append(new_notes)
    def start(self):
        self.cur_time = 0
        self.ind = 0
    def vol(self, vol0, vol1, dt, is_closed=True):
        start_time = self.cur_time
        end_time = start_time + dt
        dvol = vol1 - vol0
        if is_closed:
            end_time += epsilon
        else:
            end_time -= epsilon
        nnotes = len(self.notes)
        while self.ind < nnotes:
            note = self.notes[self.ind]
            if note.time > end_time:
                break;
            note.vol = int(vol0 + dvol*((note.time-start_time)/dt))
            self.ind += 1
        self.cur_time += dt

    # mark notes that are the highest or lowest sounding notes at their start
    #
    def flag_aux(active, started):
        min = 128
        max = -1
        for n in active:
            if n.pitch < min: min = n.pitch
            if n.pitch > max: max = n.pitch
        for n in started:
            n.highest = n.pitch == max
            n.lowest = n.pitch == min
            
    def flag_outer(self):
        cur_time = 0
        active = []     # notes active at current time
        started = []    # notes that started at current time
        for note in self.notes:
            if note.time > cur_time + epsilon:
                if len(started):
                    NoteSet.flag_aux(active, started)
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
        NoteSet.flag_aux(active, started)
            
    def outer(self, bottom, mid, top, dt):
        end_time = self.cur_time + dt
        while self.ind < len(self.notes):
            pass

    # remove notes that start while a note of the same pitch is active
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

ppp = 3
pp = 20
p = 35
mp = 50
mf = 65
f = 80
ff = 100
fff = 120

def test():
    y = NoteSet()
    y.add(Note(1,2,3,4))
    y.add(Note(0,2,3,4))
    y.sort_time()
    y.remove_overlap()
    y.print()
