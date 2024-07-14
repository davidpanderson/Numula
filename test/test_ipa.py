import ipa
from numula.notate_score import *
from numula.notate_nuance import *

def main():
    ipa.vvar('v1', .2)
    ipa.vvar('v2', .6)
    ipa.vvar('v3', .2)
    ipa.ivar('i1', '1/2')
    ipa.ivar('i2', '1/2')
    ns = n('1/8 c d e f g a b c')
    ns.vol_adjust_pft(
        vol(f'{ipa.v1} {ipa.i1} {ipa.v2} {ipa.i2} {ipa.v3}'),
        mode=VOL_SET
    )
    return ns

if __name__ == '__main__':
    import numula.pianoteq
    ns = main()
    fname = 'data/nsh_test.midi'
    ns.write_midi(fname)
    numula.pianoteq.play(fname)
