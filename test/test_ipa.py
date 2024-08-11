from numula.ipa import *
from numula.notate_score import *
from numula.notate_nuance import *

var('pvol', IPA_LAYER, 'on')
from numula.ipa import *
var('v1', IPA_VOL, .2, ['pvol'], 'starting volume')
var('v2', IPA_VOL, .6, ['pvol'], 'peak volume')
var('v3', IPA_VOL, .2, ['pvol'], desc='ending volume')
var('i1', IPA_DT_SCORE, '1/2', ['pvol'])
var('i2', IPA_DT_SCORE, '1/2', ['pvol'])

if __name__ == '__main__':
    read_vars('test_ipa')

from numula.ipa import *

def main():
    ns = n('1/32 *4 c5 d e f g a b c * 1/4 -c')
    if pvol != 'off':
        ns.vol_adjust_pft(
            vol(f'{v1} {i1} {v2} {i2} {v3}'),
            mode=VOL_SET
        )
    return ns

if __name__ == '__main__':
    import numula.pianoteq
    ns = main()
    print(ns)
    fname = 'data/test_ipa.midi'
    ns.write_midi(fname)
    numula.pianoteq.play(fname)
