from midiutil import MIDIFile
import random

def chromatic():
    track = 0
    channel = 0
    time = 0
    dur = 0.5
    tempo = 120
    vol = 120

    f = MIDIFile(1)
    f.addTempo(track, time, tempo)
    
    for pitch in range (50,70):
        f.addNote(track, channel, pitch, time, dur, vol)
        time += 1

    with open("chromatic.midi", "wb") as file:
        f.writeFile(file)

def rand_notes():
    track = 0
    channel = 0
    tempo = 120
    vol = 120
    time = 0
    
    f = MIDIFile(1)
    f.addTempo(track, time, tempo)
    
    for i in range(300):
        pitch = random.randrange(40, 80)
        time = random.uniform(0,200)
        dur = random.uniform(.1, 5)
        vol = random.randrange(20,128)
        f.addNote(track, channel, pitch, time, dur, vol)
        time += 1

    with open("random.midi", "wb") as file:
        f.writeFile(file)

rand_notes()
