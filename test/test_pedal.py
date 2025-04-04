from numula.nuance import *
from numula.MidiFile import *
from numula.pianoteq import *

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

    for i in range(127):
        t = 1.+4*i/127
        val = 127-i
        f.addControllerEvent(0, 0, t, PEDAL_SUSTAIN, val)
    t = 5
    f.addNote(0, 0, 60, t, .25, 64)
    fname = 'data/ped_test1.midi'
    with open(fname, 'wb') as file:
        f.writeFile(file)
    play_midi_file_rpc(fname)

#ped_test1()

# play a series of staccato chords.
# gradually lower the sustain pedal
def ped_test2():
    f = numula.MidiFile.MIDIFile(deinterleave=False)
    f.addTempo(0, 0, 60)
    for i in range(16):
        t = i
        dt = .05
        f.addNote(0, 0, 48, t, dt, 64)
        f.addNote(0, 0, 60, t, dt, 64)
        f.addNote(0, 0, 64, t, dt, 64)
        f.addNote(0, 0, 67, t, dt, 64)
        f.addNote(0, 0, 72, t, dt, 64)
    for i in range(128):
        t = 16.*i/128
        val = 63+i//2
        f.addControllerEvent(0, 0, t, PEDAL_SUSTAIN, val)
    fname = 'data/ped_test2.midi'
    with open(fname, 'wb') as file:
        f.writeFile(file)
    play_midi_file_rpc(fname)

ped_test2()
