import numpy
import read_midifile, pianoteq
from nuance import *

def crypto():
    ns = read_midifile.read_midifile('cryptogram.mid', 960, False)
    ns.vol_adjust_pft(
        [
            linear(pp, pp, 3/1),
            linear(pp, f, 3/1),
            linear(f, pp, 1/1),
            linear(pp, mf, 6/4),
            linear(mf, pp, 2/4),
            linear(pp, f, 5/1),
            linear(pp, mf, 9/4),
            linear(mf, p, 3/4),
            linear(p, f, 12/4),
            linear(f, pp, 34/4)
        ]
    )
    ns.roll(14/1+8*3/4+1/4, numpy.linspace(0, .5, 9))
    ns.print()
    ns.write_midi('crypto2.mid')
    pianoteq.play('crypto2.mid')

#read_midifile.print_midifile('cryptogram.mid')

crypto()
