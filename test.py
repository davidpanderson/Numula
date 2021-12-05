from midiutil import MIDIFile

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

chromatic()
