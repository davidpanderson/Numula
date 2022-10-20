import random

from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.vol_name import *
import numula.pianoteq as pianoteq

def scale():
    ns = Score([
        n('c d e f g a b c d').tag('rh'),
        n('-c d e f g a b c d').tag('lh')
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
    ns.write_midi('data/scale.midi')
    pianoteq.play('data/scale.midi')
scale()

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
    pianoteq.play('data/pan_test.midi')

#pan_test()

def preset_test():
    pianoteq.play('data/scale.midi', preset='C. Grimaldi Harpsichord A')
    #pianoteq.midi_to_wav('data/scale.midi', 'data/scale.wav', preset='Celesta Tremo')
#preset_test()
    
