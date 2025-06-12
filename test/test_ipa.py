import numula_path
from numula.ipa import *
from numula.notate_score import *
from numula.notate_nuance import *

var('pvol', IPA_TOGGLE, 'on')
tags = ['pvol']
var('v1', IPA_VOL_MULT, p, tags, 'starting volume')
var('v2', IPA_VOL_MULT, f, tags, 'peak volume')
var('v3', IPA_VOL_MULT, p, tags, 'ending volume')
var('i1', IPA_DT_SCORE, '1/2', tags)
var('i2', IPA_DT_SCORE, '1/2', tags)

if __name__ == '__main__':
    read_vars('test_ipa')

from numula.ipa import *

def main():
    ns = sh_score('1/32 *4 c5 d e f g a b c * 1/4 -c')
    if pvol != 'off':
        ns.vol_adjust_pft(
            sh_vol(f'{v1} {i1} {v2} {i2} {v3}')
        )
    return ns

if __name__ == '__main__':
    import numula.pianoteq
    ns = main()
    print(ns)
    numula.pianoteq.play_score()
