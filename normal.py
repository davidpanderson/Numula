from midiutil import MIDIFile
import random, numpy

def normal_time():
    f = MIDIFile(1)
    f.addTempo(0, 0, 120)
    for i in range(300):
        pitch = random.randrange(40, 80)
        time = 30 + numpy.random.normal()*10
        dur = 1
        vol = random.randrange(20,40)
        f.addNote(0, 0, pitch, time, dur, vol)

    with open("normal.midi", "wb") as file:
        f.writeFile(file)

normal_time()
