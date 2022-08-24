import random
from nscore import *
from notate import *
from nuance import *
import pianoteq

def scale():
    ns = Score([
        #n('c d e', ['rh'])
        n('c d e f g a b c d', ['rh']),
        n('-c d e f g a b c d', ['lh'])
    ])
    ns.done()

    ns.vol_adjust_pft(
        [
            linear(pp, ff, 4/4),
            linear(f, p, 4/4, closed_start=False)
        ], pred=lambda n: 'rh' in n.tags
    )

    ns.print()
    print('---')
    ns.tempo_adjust_pft(
        [
            #linear(1, 2, 2/4)
            linear(60, 120, 4/4),
            linear(120, 60, 4/4)
        ], normalize=True,
        pred=lambda n: 'rh' in n.tags
    )

    ns.print()
    ns.write_midi('data/scale.midi')
    pianoteq.play('data/scale.midi')

# make some notes with different pitches and same vol
# (test input for panning)
# Also make a "pan position file"
def pan_test():
    ns = Score()
    for i in range(240):
        ns.append_note(Note(0, 1/16, random.randrange(48, 72), .5))
        ns.advance_time(1/16)
    ns.done()
    ns.write_midi('data/pan_test.midi')
    pos_array = ns.get_pos_array(
        [
            linear(-1, 1, 61/4)
        ], 44100
    )
    pianoteq.play('data/pan_test.midi')

#pan_test()

def preset_test():
    pianoteq.play('data/scale.midi', preset='C. Grimaldi Harpsichord A')
    #pianoteq.midi_to_wav('data/scale.midi', 'data/scale.wav', preset='Celesta Tremo')
preset_test()
    
