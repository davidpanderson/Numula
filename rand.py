from midiutil import MIDIFile
import random

def rand_notes():
    track = 0
    channel = 0
    tempo = 120
    time = 0
    
    f = MIDIFile(1)
    f.addTempo(track, time, tempo)
    
    for i in range(300):
        pitch = random.randrange(40, 80)
        time = random.uniform(0,200)
        dur = random.uniform(.1, 5)
        vol = random.randrange(20,128)
        f.addNote(track, channel, pitch, time, dur, vol)

    with open("random.midi", "wb") as file:
        f.writeFile(file)

rand_notes()
