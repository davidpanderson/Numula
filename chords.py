from midiutil import MIDIFile
import random, math

def main():
    f = MIDIFile(1)
    f.addTempo(0, 0, 240)

    c=[0]*4
    time = 0
    dur = 8
    vol = 40
    j = 0
    for i in range(4):
        c[i] = 0
    for i in range(1000):
        #j = random.randrange(4)
        j = (j+1) % 4
        octave = random.randrange(4,8)
        pitch = octave*12 + c[j]
        vol = (math.sin(time/30)+1)*20 + 10 + random.randrange(20)
        vol = int(vol)
        
        f.addNote(0, 0, pitch, time, dur, vol)
        #time += random.uniform(.5, 2.)
        time += .5*random.randrange(0,6)
        if i % 30 == 29:
            c[random.randrange(4)] = random.randrange(12)

    with open("chords.midi", "wb") as file:
        f.writeFile(file)

main()
