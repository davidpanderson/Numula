import random

import numula_path
from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq as pianoteq

def scale():
    ns = Score([
        sh_score('c d e f g a b c d').tag('rh'),
        sh_score('-c d e f g a b c d').tag('lh')
    ])

    ns.vol_adjust_pft(
        [
            Linear(pp, ff, 4/4),
            Linear(f, p, 4/4, closed_start=True)
        ], pred=lambda n: 'rh' in n.tags
    )

    print(ns)
    print('---')
    ns.tempo_adjust_pft(
        [
            Linear(60, 120, 4/4),
            Linear(120, 60, 4/4)
        ], normalize=True,
        pred=lambda n: 'rh' in n.tags
    )

    print(ns)
    pianoteq.play_score(ns)
#scale()

# make some notes with different pitches and same vol
# (test input for panning)
# Also make a "pan position file"
def pan_test():
    ns = Score()
    for i in range(240):
        ns.append_note(Note(0, 1/16, random.randrange(48, 72), .5))
        ns.advance_time(1/16)
    ns.write_midi('data/pan_test.midi')
    pos_array = ns.get_pos_array(
        [
            Linear(-1, 1, 61/4)
        ], 44100
    )
    pianoteq.play_midi_file('data/pan_test.midi')

#pan_test()

def preset_test():
    pianoteq.play_midi_file('data/scale.midi', preset='C. Grimaldi Harpsichord A')
    #pianoteq.midi_to_wav('data/scale.midi', 'data/scale.wav', preset='Celesta Tremo')
#preset_test()

def meas_test():
    sh_score(' \
        1/4 . \
        |10 m3/4 . . . \
        |11 m4/4 \
        . . . . \
        |12 \
    ')
#meas_test()

def tempo_test():
    x = sh_tempo('*2 60 8/4 80 p.01 60 3/4 120 0.2p *')
    print(*x, sep='\n')
#tempo_test()

def pause_test():
    x = sh_tempo('.2p 4/4 . . .1p .')
    print(*x, sep='\n')
#pause_test()

def pedal_test():
    x = pedal('- 1/4 + 1/8 + 1/4 - 4/4')
    print(*x, sep='\n')

# character input test
# Note: this doesn't work when run from Idle.
# You need to run it from cmd or powershell: python.exe test.py
#
from readchar import readkey, readchar, key
def input_test():
    while True:
        x = readkey()
        print('got ', x)

#input_test()

def global_test():
    globals()['foo'] = 'bar'

def gtest():
    global_test()

gtest()
print(globals())

    
