import numpy
import read_midifile, pianoteq
from nuance import *

def crypto():
    ns = read_midifile.read_midifile('data/cryptogram.mid', 960, False)
    ns.vol_adjust_pft(
        [
            Linear(pp, pp, 3/1),
            Linear(pp, f, 3/1),
            Linear(f, pp, 1/1),
            Linear(pp, mf, 6/4),
            Linear(mf, pp, 2/4),
            Linear(pp, f, 5/1),
            Linear(pp, mf, 9/4),
            Linear(mf, p, 3/4),
            Linear(p, f, 12/4),
            Linear(f, pp, 34/4)
        ]
    )
    ns.roll(14/1+8*3/4+1/4, numpy.linspace(0, .5, 9))
    print(ns)
    ns.write_midi('data/crypto2.mid')
    pianoteq.play('data/crypto2.mid')

#read_midifile.print_midifile('data/cryptogram.mid')

crypto()
