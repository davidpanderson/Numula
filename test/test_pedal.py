from numula.nuance import *

def ped_test():
    ns = sh_score('3* [c4 c5 e5 g5 c6] . . . * ')
    ns.insert_pedal(PedalUse(1, 1/4))
    numula.pianoteq.play_score(ns);

# play a chord with the sustain pedal down.
# from time 1 to 2, lift the pedal
def ped_test1():
    f = numula.MidiFile.MIDIFile(deinterleave=False)
    t = 0
    f.addControllerEvent(0, 0, t, PEDAL_SUSTAIN, 127)
    f.addNote(0, 0, 60, t, .25, 64)
    f.addNote(0, 0, 64, t, .25, 64)
    f.addNote(0, 0, 67, t, .25, 64)
    f.addNote(0, 0, 72, t, .25, 64)

    for i in range(64):
        t = 1.+i/64
        val = 127-i
        f.addControllerEvent(0, 0, t, PEDAL_SUSTAIN, val)

    t = 2
    f.addNote(0, 0, 60, t, .25, 64)
    fname = 'data/ped_test1.midi'
    with open(fname, 'wb') as file:
        f.writeFile(file)
    play_midi_file_rpc(fname)

ped_test1()

# play a series of staccato chords.
# gradually lower the sustain pedal
