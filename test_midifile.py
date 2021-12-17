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

# show a bug in MIDIFile: crashes if 2 notes w/ same time and pitch
#
def mf_bug():
    f = MIDIFile(1)
    f.addTempo(0, 0, 120)
    f.addNote(0, 0, 60, 0, .5, 64);
    f.addNote(0, 0, 60, 0, .4, 64);
    with open("test.midi", "wb") as file:
        f.writeFile(file)
        

