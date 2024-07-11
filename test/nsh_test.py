import nshl

from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *

def main():
    nshl.var('v1', .2, .05, 0, 2)
    nshl.var('v2', .6, .05, 0, 2)
    nshl.var('v3', .2, .05, 0, 2)
    ns = n('1/8 c d e f g a b c')
    ns.vol_adjust_pft(
        vol(f'{nshl.v1} 1/2 {nshl.v2} 1/2 {nshl.v3}'),
        mode=VOL_SET
    )
    return ns

if __name__ == "__main__":
    import numula.pianoteq
    ns = main()
    fname = 'data/nsh_test.midi'
    ns.write_midi(fname)
    numula.pianoteq.play(fname)
