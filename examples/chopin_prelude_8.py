'''
Chopin prelude #8

nuance structure:

timing
    pauses
        1-beat patterns: pb0, pb_start etc.
        1-measure patterns: pm1, pm2; made up of beat patterns
        'pauses': PFT with measure patterns and some extra pauses
    tbeat: accelerando within each beat.
        Same throughput the piece.
        Not sure if this is important, but the idea is
        to create a feeling of always surging forward
    tphrase: tempo at phrase level
        1-measure patterns: t1, t2,...
        tphrase: PFT with measure patterns
        Currently this is common between LH and RH;
        might be interesting to decouple at the tphrase level

volume
    accent patterns
        lh_accents, rh_accents
        each is a 1-beat pattern that repeats throughout
    vmeas: continuous change within measures
        1-measure patterns: vm_4_sm, vm_3 etc.
        vmeas: PFT that uses these
    vphrase: continuous change at 1-8 measure level
        a single PFT
'''

import numula_path
from numula.ipa import *
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *

var('if_pauses', IPA_TOGGLE, 'on')
var('if_tbeat', IPA_TOGGLE, 'on')
var('if_tphrase', IPA_TOGGLE, 'on')
var('if_accents', IPA_TOGGLE, 'on')
var('if_vmeas', IPA_TOGGLE, 'on')
var('if_vphrase', IPA_TOGGLE, 'on')
var('if_rh', IPA_TOGGLE, 'on')
var('if_lh', IPA_TOGGLE, 'on')

if __name__ == '__main__':
    read_vars('chopin_prelude_8')

from numula.ipa import *

right_hand = sh_score('meas4/4 \
    |1 1/32 \
        *2 c4+ +c+ g+ b a f+ d +d \
            --c+ +c+ g+ b a g+ f+ +f+ \
            -f+ +f+ -a+ c+ b g+ e+ +e+ \
            -a +a -b+ d c+ b g+ +g+ \
        * \
    |3 -c+ +c+ g+ b a f+ d+ +d+ \
        --c+ +c+ -e+ g+ f+ d+ b+ +b+ \
        --b +b f+ a g e c+ +c+ \
        --b +b -d+ f+ e c+ a+ +a+ \
    |4 --a +a -c++ e+ d+ c b +b \
        --a +a -c+ e d b g+ +g+ \
        --f+ +f+ -a+ c+ b g+ e+ +e+ \
        --d +d -f++ a g+ e+ c+ +c+ \
    |5  c4+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -f+ +f+ -a+ c+ b g+ e+ +e+ \
        -a +a -b+ d c+ b g+ +g+ \
    |6  c4+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -a +a -c+ e d b g+ +g+ \
        -c+ +c+ -d+ f+ e d b +b \
    |7  e5 +e b d c a f+ +f+ \
        --e +e -g+ b a f+ d+ +d+ \
        --d +d -f++ a+ g+ f e +e \
        --d +d -f+ a g e c+ +c+ \
    |8  c5 +c -e+ g+ f+ e- d +d \
        --c +c -e g f d b +b \
        -c- +c- -e- g- f- d- b- +b- \
        -b- +b- -e- g- f- d- b- +b- \
    |9  b4- +b- -e g f d a +a \
        -b-- +b-- -d- f- e-- c- a- +a- \
        -a- +a- -c+ e- d b g +g \
        -g +g d f e- d c +c \
    |10  c5 +c -f+ a- g e- b +b \
        -c- +c- -e- g- f- e- b- +b- \
        -b- +b- -d+ f e c+ a +a \
        -a +a e g f e d +d \
    |11  d5 +d -e g f e- c +c \
        -c +c -e g f d b- +b- \
        -b- +b- -c+ e- d c a +a \
        -a +a -c+ e- d b g +g \
    |12  g4 +g -a c b- a- f +f \
        --e +e -a c b- a- f +f \
        -f +f -a c- b- a- f +f \
        -g- +g- d f e- b- g- +g- \
    |13 g4- +g- -g b- a- g- f- +f- \
        -f- +f- -g b- a- f- -a- +a- \
        -c- +c- -f a- g- e- c- +c- \
        --b- +b- f a- g- e- c- +c- \
    |14 c4 +c -f a- g- f- c +c \
        -d- +d- -f a- g- f- d +d \
        -d +d -f a- g- f- d +d \
        -e- +e- b- d- c- g- e- +e- \
    |15 e4- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f\
        -g- +g- -b- e- d b- f +f \
    |16 e4- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f \
        -b- +b- -e g- f d b- +b- \
    |17 e4- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f\
        -g- +g- -b- e- d b- f +f \
    |18 e4- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f \
        -e+ +e+ -b d c+ b -c+ +c+ \
    |19 c4+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -f+ +f+ -a+ c+ b g+ e+ +e+ \
        -a +a -b+ d c+ b g+ +g+ \
    |20 c4+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -a +a -c+ e d b g+ +g+ \
        -c+ +c+ -d+ f+ e d b +b \
    |21 b4 +b -d+ f+ e c+ a+ +a+ \
        -d +d -e+ g f+ e c+ +c+ \
        -c+ +c+ -e+ g+ f+ d+ b+ +b+ \
        -e+ +e+ -g+ b a g+ f+ +f+ \
    |22 g5+ +g+ -c++ e+ d+ b+ a +a \
        --g+ +g+ -c++ e+ d+ b+ a +a \
        --g+ +g+ -c+ e d b+ a +a \
        --g+ +g+ -c+ e d b+ a +a \
    |23 a5 +a -e+ g+ f+ c+ a +a \
        --g+ +g+ d+ f+ e c+ g+ +g+ \
        --e +e b d c+ a e +e \
        --c+ +c+ g+ b a f+ c+ +c+ \
    |24 g4+ +g+ d+ f+ e c+ g+ +g+ \
        --f+ +f+ c+ e d a f+ +f+ \
        --e +e b d c+ a e +e \
        --d +d a c+ b g d +d \
    |25 *4 c4+ +c+ g+ b a f+ c+ +c+ * \
    |26 *2 c4+ +c+ -f++ a g+ f+ c+ +c+ * \
        *2 c4+ +c+ -f++ a g+ e+ c+ +c+ * \
    |27 *4 c4+ +c+ g+ b a f+ c+ +c+ * \
    |28 *3 d4 +d a+ c+ b f+ d +d * \
        f4+ +f+ -a+ c+ b f+ d +d \
    |29 *4 c4+ +c+ g+ b a+ f+ c+ +c+ * \
    |30 *3 d4+ +d+ a+ c+ b f+ d+ +d+ * \
        f4+ +f+ -a+ c+ b f+ d+ +d+ \
    |31 *4 c4+ +c+ g+ b a+ f+ c+ +c+ * \
    |32 *4 c4+ +c+ g+ b a f+ c+ +c+ * \
    |33 1/2 [c4+ e +c+] 1/4 [b g d] [e+ c+ b] \
    |34 1/4 (grace e4+ grace) 2/1 [f2+ +c+ +a c+ (last f+ last)]\
').tag('right_hand')

# timing in last measure:
# play all notes as rolled chord
# use adjust_dur_abs() to make the grace note E# end at the F#

left_hand = sh_score('meas4/4 \
    < 1/24 1/24 1/24 1/8 > \
    |1 *2 a3 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ * \
    |3 a4 -d+ f+ -a +g+ d+ f+ -g+ g4 -c+ e -g +f+ c+ e -f+ \
    |4 f4 c d+ -f +f -b d -f +d -g+ b -d +b -c+ e+ --c+ \
    |5 a3 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ \
    |6 a3 -c+ f+ -f+ ++a -c+ f+ -a ++f -b d -f +e -g+ +d -e \
    |7 c5 -f+ a -c +b f+ a -b +b- f g+ -b- +a e g -a \
    |8 a4- e- f+ -a- +g d f -g +a-- -d- f- -a-- +g- d- f- -g- \
    |9 f4 -b- d -f +f -b d -f +f -g b -f +e- -g c -f \
    |10 g4 -c e- -f ++g -c+ e -f ++g -a c+ -f +f -a d -f \
    |11 f4 -a +e- -f +d -f b- -b- ++d -f+ +c -d +b- -d g -g \
    |12 b3- -d +a- -b- +b- -d +a- -b- +a- -b- d -e- ++g- -b- e- -e- \
    |13 a3- -a- d- -f- ++a- -a- d- -f- ++g- -c- e- -g- +g- -c- e- -g- \
    |14 g3- -b- +f- -g- +g- -b- +f- -g- +f- -g- b- -c- ++e- -g- c- -c- \
    |15 *3 a3- -c- e- -f ++a- -c- e- -f ++d -f b- -b- ++d -f b- -b- *\
    |18 a3- -c- e- -f ++a- -c- e- -f ++d -f b- -b- ++b -c+ e+ -g+ \
    |19 a3 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ \
    |20 a3 -c+ f+ -f+ ++a -c+ f+ -a ++f -b d -f +e -g+ +d -e \
    |21 g4 -c+ e -g +f+ -a+ +e -f+ a4 -d+ f+ -a ++b+ -f+ a -b+ \
    |22 *2 f5+ -a b+ -d+ * *2 f5+ -a b+ -d * \
    |23 f5+ -a c+ -c+ ++e -g+ c+ -c+ +c+ -e a -a +a -c+ f+ -f+ \
    |24 e4 -g+ c+ -c+ ++d -f+ a -d +c+ -e a -a ++b -d g -b \
    |25 *2 a3 -a c+ -c+ * g3+ -a c+ -c+ ++f+ -a c+ -c+ \
    |26 *2 f3+ -g+ c+ -c+ * *2 e3+ -g+ c+ -c+ * \
    |27 *4 a3 -c+ f+ -f+ * \
    |28 *4 f3+ -f+ b -b * \
    |29 *4 a3+ -c+ f+ -f+ * \
    |30 *4 f3+ -f+ b -b * \
    |31 *4 a3+ -c+ f+ -f+ * \
    |32 *4 a3 -c+ f+ -f+ * \
    |33 1/2 [a2 +e a] 1/4 [g -b] [c+ +g+] \
    |34 1/1 . \
    |35 \
').tag('left_hand')

################ VOLUME #################

# RH accents
tags = ['if_accents', 'if_rh']
var('rha1', IPA_VOL, .12, tags)
var('rha2', IPA_VOL, .1, tags)
var('rha3', IPA_VOL, .05, tags)
var('rha4', IPA_VOL, 0, tags)
var('rha5', IPA_VOL, .05, tags)
var('rha6', IPA_VOL, 0, tags)
var('rha7', IPA_VOL, .10, tags)
var('rha8', IPA_VOL, .07, tags)
from numula.ipa import *

# 1 measure of RH accents
rha = f'*4 {rha1} 1/32 {rha2} 1/32 {rha3} 1/32 {rha4} 1/32 {rha5} 1/32 {rha6} 1/32 {rha7} 1/32 {rha8} 1/32 *'

rh_accents = sh_accents(f'meas4/4 \
    |1 *32 {rha} * \
    |33 \
')

# LH accents
tags = ['if_accents', 'if_lh']
var('lha1', IPA_VOL, .04, tags)
var('lha2', IPA_VOL, -.1, tags)
var('lha3', IPA_VOL, -.1, tags)
var('lha4', IPA_VOL, 0, tags)
from numula.ipa import *

lh_accents = sh_accents(f'meas4/4 \
    |1 *32 \
        *4 {lha1} 1/24 {lha2} 1/24 {lha3} 1/24 {lha4} 1/8 * \
        * \
    |33 \
')

# volume
tags = ['if_vmeas']
var('dv1', IPA_VOL, 1.08, tags)        # volume swells in vmeas
var('dv2', IPA_VOL, 1.10, tags)
var('dv3', IPA_VOL, 1.15, tags)
from numula.ipa import *

# swell to 4th beat
vm_4_sm = f'[ mm 3/4 {dv1} 1/4 mm'

# bigger swell
vm_4_med = f'[ mm 3/4 {dv2} 1/4 mm'

# even bigger
vm_4_lg = f'[ mm 3/4 {dv3} 1/4 mm'

# swells to 2nd and 4th beat
vm_24 = f'[ *2 mm 1/4 {dv1} 1/4 mm *'

# swell to 3rd beat
vm_3 = f'[ mm 2/4 {dv2} 2/4 mm'

# no swell
vm_0 = '[ mm 1/1 mm'

vmeas = sh_vol(f'meas4/4 \
    |1 {vm_4_sm} {vm_4_med} {vm_24} {vm_3} \
    |5 {vm_4_med} {vm_4_lg} {vm_24} {vm_3} \
    |9 {vm_3} {vm_3} {vm_24} {vm_3} \
    |13 {vm_24} {vm_4_med} \
    |15 *4 {vm_4_med} * \
    |19 {vm_4_med} {vm_4_lg} {vm_24} {vm_24} \
    |23 *4 {vm_0} * \
    |27 *2 {vm_0} {vm_4_sm} * \
    |31 *2 {vm_0} * \
    |33 *2 [ mm 1/1 mm * \
')

vphrase = sh_vol('meas4/4 \
    |1 pp 8/1 pp \
    |9 [ pp 4/1 mf \
    |13 mf 2/1 f \
    |15 f 2/1 f \
    |17 [ p 3/1 p \
    |20 p 2/1 mf 1/1 f \
    |23 f 4/1 p \
    |27 2/1 p \
    |29 [ pp 2/1 pp \
    |31 exp4.0 pp 1/1 mf exp-3.5 1/1 pp linear \
    |33 [ mp 2/1 p \
    |35 \
')

################ TIMING #################

# pause patterns for the 8 32ths in one beat
# 0 melody
# 1 melody octave
# 2
# 3
# 4
# 5
# 6 melody
# 7 melody octave

# pause durations
dt0 = .02
dt1 = .04
dt2 = .06
dt3 = .08
dt4 = .10
dt5 = .12
dt6 = .15

tags = ['if_pauses']
var('p_start', IPA_DT_SEC, .04, tags)
    # pause on measure start melody note
var('p_start2', IPA_DT_SEC, .06, tags)
    # pause on phrase start melody note
var('p_start3', IPA_DT_SEC, .08, tags)
    # pause on major phrase start melody note
var('p_mel', IPA_DT_SEC, .02, tags)
    # pause on other melody notes (top and bottom)
var('p_end', IPA_DT_SEC, .06, tags)
    # pause on minor phrase end melody note
var('p_end2', IPA_DT_SEC, .08, tags)
    # pause on major phrase end melody note
from numula.ipa import *

# Go lightly with pauses, else they affect tempo

# default: short pauses after melody notes
pb0 = f'p{p_start} 1/32 . p{p_mel} 5/32 . p{p_mel} 1/32 . p{p_mel} 1/32 .'

# major phrase start: longer pause on 1st melody note
pb_start = f'p{p_start3} 1/32 . p{p_mel} 5/32 . p{p_mel} 1/32 . p{p_mel} 1/32 .'

# phrase start
pb_start_short = f'p{p_start2} 1/32 . p{p_mel} 5/32 . p{p_mel} 1/32 . p{p_mel} 1/32 .'

# phrase end: longer pause after last note
pb_end = f'p{p_start} 1/32 . p{p_mel} 5/32 . p{p_mel} 1/32 . p{p_end2} 1/32 .'

# phrase end with shorter pause at end
pb_end_short = f'p{p_start} 1/32 . p{p_mel} 5/32 . p{p_mel} 1/32 . p{p_end} 1/32 .'

# measure 1 has a big pause after 1st note
pm1 = f'{pb_start} {pb0} {pb_start_short} {pb_end}'

# measure 2 has a lesser pause
pm2 = f'{pb0} {pb0} {pb_start} {pb_end}'

# measure 3: 2+2 beats
pm3 = f'{pb0} {pb_end} {pb0} {pb_end}'

# measure 8: moving forward, part of longer phrase
pm8 = f'{pb_start_short} {pb0} {pb0} {pb_end_short}'

pauses = sh_tempo(f'meas4/4 \
    |1 {pm1} {pm2} \
    |3 {pm3} {pm2} \
    |5 {pm1} {pm2} \
    |7 {pm3} {pm8} \
    |9 *4 {pm8} * \
    |13 {dt2}p *4 {pm8} * \
    |17 {dt3}p *2 {pm8} * \
    |19 {pm1} {pm2} {pm3} {pm8} \
    |23 {dt4}p {pm8} {dt1}p {pm8} \
    |25 {dt1}p *2 {pm8} * \
    |27 {dt2}p *2 {pm8} * \
    |29 {dt2}p *2 {pm8} * \
    |31 {pm8} {dt4}p {pm8} {dt6}p \
    |33 \
')

# beat-level tempo
tags = ['if_tbeat']
var('tbeat1', IPA_TEMPO, 57, tags)        # start
var('tbeat2', IPA_TEMPO, 63, tags)        # end
from numula.ipa import *

# accel within each beat
tbeat = sh_tempo(f'meas4/4 \
    |1 *32 *4 {tbeat1} 1/4 {tbeat2} * * \
')

# phrase-level tempo
tags = ['if_tphrase']
var('tph_1_1', IPA_TEMPO, 40, tags)
var('tph_1_2', IPA_TEMPO, 60, tags)
var('tph_2_1', IPA_TEMPO, 50, tags)
var('tph_2_2', IPA_TEMPO, 65, tags)
var('tph_2_3', IPA_TEMPO, 50, tags)
var('tph_2_4', IPA_TEMPO, 40, tags)
from numula.ipa import *

# accel mid-measure, rit at end
t1 = f' {tph_1_1} 2/4 {tph_1_2} 2/4 {tph_1_1}'

# more angst
t2 = f' {tph_2_1} 3/4 {tph_2_2} {tph_2_3} 1/4 {tph_2_4}'

# two 2-beat surges
t3 = '50 1/4 55 1/4 45 1/4 55 1/4 45'

# rit over 1 measure (phrase end)
trit = 'exp0.5 55 1/1 40 linear'

# accel mid-measure
t7 = '50 2/4 60 2/4 50'

# bigger rit
trit2 = '60 1/1 35'
 
# faster version of t1
t19 = '50 2/4 70 2/4 50'

tphrase = sh_tempo(f'meas4/4 \
    |1 {t1} {t2} {t3} {trit} \
    |5 {t1} {t1} {t7} {t7} \
    |9 {t7} {t7} {t3} {t1} \
    |13 {t3} {t1} \
    |15 {t7} {t1} {t7} {trit2} \
    |19 *3 {t19} * 65 1/1 50 \
    |23 50 2/1 45 \
    |25 55 2/1 40 \
    |27 {t1} {trit} {t1} {trit2} \
    |31 50 1/1 70 60 1/1 45 \
    |33 30 2/1 20 \
    |35 \
')

def main():
    nuance = False
    if nuance:
        ns = Score(tempo=110)
    else:
        ns = Score(tempo=75)
    # virtual pedal within a beat
    right_hand.dur_pattern([6/32, 6/32, 2/32, 1/32, 4/32, 3/32, 2/32, 2/32], 0, 32/1)
    left_hand.dur_pattern([6/24, 2/24, 1/24, 3/24], 0, 32/1)
    parts = []
    if if_rh != 'off':
        parts.append(right_hand)
    if if_lh != 'off':
        parts.append(left_hand)
    ns.append_scores(parts)
    #ns.trim(0, 8/1)
    #print(ns)
    if nuance:
        if if_vphrase != 'off':
            ns.vol_adjust_pft(vphrase)
        if if_vmeas != 'off':
            ns.vol_adjust_pft(vmeas, mode=VOL_SCALE)
        if if_accents != 'off':
            ns.vol_adjust_pft(rh_accents, selector=lambda n: 'right_hand' in n.tags, mode=VOL_ADD)
            ns.vol_adjust_pft(lh_accents, selector=lambda n: 'left_hand' in n.tags, mode=VOL_ADD)
            ns.vol_adjust(1.3, lambda n: 'top' in n.tags and n.time >= 32, mode=VOL_MULT)
            ns.vol_adjust(1.2, lambda n: 'grace' in n.tags, mode=VOL_SET)
            ns.vol_adjust(1.0, lambda n: 'last' in n.tags, mode=VOL_SET)
        if if_tbeat != 'off':
            ns.tempo_adjust_pft(tbeat)
        if if_tphrase != 'off':
            ns.tempo_adjust_pft(tphrase)
        if if_pauses != 'off':
            ns.tempo_adjust_pft(pauses)
        ns.roll(33/1+1/4, [0, .1, .2, .3, .5])
        if True:
            ns.adjust_dur_abs(1.9, lambda n: 'grace' in n.tags)
    #print(ns)
    return ns

if __name__ == '__main__':
    import numula.pianoteq
    ns = main()
    numula.pianoteq.play_score(ns, 'NY Steinway D Classical')
