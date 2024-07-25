from ipa import *
from numula.notate_score import *
from numula.notate_nuance import *

def main():
    tag('foobar')
    var('v1', VOL, .2, ['foobar'])
    var('v2', VOL, .6)
    var('v3', VOL, .2)
    var('i1', DUR, '1/2')
    var('i2', DUR, '1/2')
    ns = n('1/8 c5 d e f g a b c 1/2 -c')
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
