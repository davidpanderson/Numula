# temporal Shepard tone:
# a melody that always gets faster, but ends up where it started

# N: # of notes
# M: # of repetitions before

from MidiFile import MIDIFile

t = 0
i = 0

def shepard(pitches, nrep, f):
    global t, i
    m = len(pitches)
    nnotes = m*nrep
    k= 0
    for r in range(nrep):
        for j in range(m):
            dt = pow(m, -k/nnotes)
            if i % (m+1) == 0:
                dur = 1
                vol = 1
            else:
                dur = dt
                vol = 1 - k/nnotes
            v = int(vol*127)
            p = pitches[i%m]
            print(i, j, p, dt, vol)
            f.addNote(0, 0, p, t, dur, v)
            t += dt
            i += 1
            k += 1

def main(pitches, nrep, ncycles):
    f = MIDIFile()
    for i in range(ncycles):
        shepard(pitches, nrep, f)
    with open("shepard.midi", "wb") as file:
        f.writeFile(file)
        
main([60, 62, 58, 46, 53], 24, 2)
