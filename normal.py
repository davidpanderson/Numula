import random, numpy, math
import note

def normal_time():
    notes = note.NoteSet()
    z = []
    min = 0
    for i in range(400):
        x = numpy.random.normal()
        if x > 2: continue
        if x < -2: continue
        z.append(x)
        if x < min: min = x
    for x in z:
        y = math.exp(-(x*x))
        r = int(y*36)
        if r > 0:
            pitch = 60 + random.randrange(-r, r+1)
        else:
            pitch = 60
        time = 30*(x-min)   # 4 min long
        dur = random.randrange(1,6)
        vol = 10 + random.randrange(1+int(y*110))
        notes.add(note.Note(time, dur, pitch, vol))
        #print(x, pitch, time, dur, vol)

    notes.remove_overlap()
    notes.write_midi("normal.midi")

normal_time()
