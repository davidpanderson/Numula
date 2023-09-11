# Robert Helps: Hommage a Rachmaninoff

from numula.nscore import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq
import numula.pianoteq_rpc

soprano = n('meas4/4 \
    |1 1/32 \
        *2 c5+ +c+ g+ b a f+ d +d \
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
    |5  c5+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -f+ +f+ -a+ c+ b g+ e+ +e+ \
        -a +a -b+ d c+ b g+ +g+ \
    |6  c5+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -a +a -c+ e d b g+ +g+ \
        -c+ +c+ -d+ f+ e d b +b \
    |7  e6 +e b d c a f+ +f+ \
        --e +e -g+ b a f+ d+ +d+ \
        --d +d -f++ a+ g+ f e +e \
        --d +d -f+ a g e c+ +c+ \
    |8  c6 +c -e+ g+ f+ e- d +d \
        --c +c -e g f d b +b \
        -c- +c- -e- g- f- d- b- +b- \
        -b- +b- -e- g- f- d- b- +b- \
    |9  b5- +b- -e g f d a +a \
        -b-- +b-- -d- f- e-- c- a- +a- \
        -a- +a- -c+ e- d b g +g \
        -g +g d f e- d c +c \
    |10  c6 +c -f+ a- g e- b +b \
        -c- +c- -e- g- f- e- b- +b- \
        -b- +b- -d+ f e c+ a +a \
        -a +a e g f e d +d \
    |11  d6 +d -e g f e- c +c \
        -c +c -e g f d b- +b- \
        -b- +b- -c+ e- d c a +a \
        -a +a -c+ e- d b g +g \
    |12  g5 +g -a c b- a- f +f \
        --e +e -a c b- a- f +f \
        -f +f -a c- b- a- f +f \
        -g- +g- d f e- b- g- +g- \
    |13 g5- +g- -g b- a- g- f- +f- \
        -f- +f- -g b- a- f- -a- +a- \
        -c- +c- -f a- g- e- c- +c- \
        --b- +b- f a- g- e- c- +c- \
    |14 c5 +c -f a- g- f- c +c \
        -d- +d- -f a- g- f- d +d \
        -d +d -f a- g- f- d +d \
        -e- +e- b- d- c- g- e- +e- \
    |15 e5- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f\
        -g- +g- -b- e- d b- f +f \
    |16 e5- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f \
        -b- +b- -e g- f d b- +b- \
    |17 e5- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f\
        -g- +g- -b- e- d b- f +f \
    |18 e5- +e- -a- d- c- a- e- +e- \
        --d +d -a- d- c- a- e- +e- \
        -f +f -b- e- d b- f +f \
        -e+ +e+ -b d c+ b -c+ +c+ \
    |19 c5+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -f+ +f+ -a+ c+ b g+ e+ +e+ \
        -a +a -b+ d c+ b g+ +g+ \
    |20  c5+ +c+ g+ b a f+ d +d \
        --c+ +c+ g+ b a g+ f+ +f+ \
        -a +a -c+ e d b g+ +g+ \
        -c+ +c+ -d+ f+ e d b +b \
    |21 b5 +b -d+ f+ e c+ a+ +a+ \
        -d +d -e+ g f+ e c+ +c+ \
        -c+ +c+ -e+ g+ f+ d+ b+ +b+ \
        -e+ +e+ -g+ b a g+ f+ +f+ \
    |22 g6+ +g+ -c++ e+ d+ b+ a +a \
        --g+ +g+ -c++ e+ d+ b+ a +a \
        --g+ +g+ -c+ e d b+ a +a \
        --g+ +g+ -c+ e d b+ a +a \
    |23 a6 +a -e+ g+ f+ c+ a +a \
        --g+ +g+ d+ f+ e c+ g+ +g+ \
        --e +e b d c+ a e +e \
        --c+ +c+ g+ b a f+ c+ +c+ \
    |24 g5+ +g+ d+ f+ e c+ g+ +g+ \
        --f+ +f+ c+ e d a f+ +f+ \
        --e +e b d c+ a e +e \
        --d +d a c+ b g d +d \
    |25 *4 c5+ +c+ g+ b a f+ c+ +c+ * \
    |26 *2 c5+ +c+ -f++ a g+ f+ c+ +c+ * \
        *2 c5+ +c+ -f++ a g+ e+ c+ +c+ * \
    |27 *4 c5+ +c+ g+ b a f+ c+ +c+ * \
    |28 *3 d5 +d a+ c+ b f+ d +d * \
        f5+ +f+ -a+ c+ b f+ d +d \
    |29 *4 c5+ +c+ g+ b a+ f+ c+ +c+ * \
    |30 *3 d5+ +d+ a+ c+ b f+ d+ +d+ * \
        f5+ +f+ -a+ c+ b f+ d+ +d+ \
    |31 *4 c5+ +c+ g+ b a+ f+ c+ +c+ * \
    |32 *4 c5+ +c+ g+ b a f+ c+ +c+ * \
    |33 1/2 [c5+ e +c+] 1/4 [b g d] [e+ c+ b] \
    |34 1/4 e5+ 2/1 [f3+ +c+ +a c+ f+ ]\
').tag('soprano')

# timing in last measure:
# play all notes as rolled chord
# use perf_dur_abs() to make the grace note E# end at the F#

bass = n('meas4/4 \
    < 1/24 1/24 1/24 1/8 > \
    |1 *2 a4 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ * \
    |3 a5 -d+ f+ -a +g+ d+ f+ -g+ g5 -c+ e -g +f+ c+ e -f+ \
    |4 f5 c d+ -f +f -b d -f +d -g+ b -d +b -c+ e+ --c+ \
    |5 a4 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ \
    |6 a4 -c+ f+ -f+ ++a -c+ f+ -a ++f -b d -f +e -g+ +d -e \
    |7 c6 -f+ a -c +b f+ a -b +b- f g+ -b- +a e g -a \
    |8 a5- e- f+ -a- +g d f -g +a-- -d- f- -a-- +g- d- f- -g- \
    |9 f5 -b- d -f +f -b d -f +f -g b -f +e- -g c -f \
    |10 g5 -c e- -f ++g -c+ e -f ++g -a c+ -f +f -a d -f \
    |11 f5 -a +e- -f +d -f b- -b- ++d -f+ +c -d +b- -d g -g \
    |12 b4- -d +a- -b- +b- -d +a- -b- +a- -b- d -e- ++g- -b- e- -e- \
    |13 a4- -a- d- -f- ++a- -a- d- -f- ++g- -c- e- -g- +g- -c- e- -g- \
    |14 g4- -b- +f- -g- +g- -b- +f- -g- +f- -g- b- -c- ++e- -g- c- -c- \
    |15 *3 a4- -c- e- -f ++a- -c- e- -f ++d -f b- -b- ++d -f b- -b- *\
    |18 a4- -c- e- -f ++a- -c- e- -f ++d -f b- -b- ++b -c+ e+ -g+ \
    |19 a4 -c+ f+ -f+ ++a -c+ f+ -a ++d -g+ b -d +c+ -e+ b -c+ \
    |20 a4 -c+ f+ -f+ ++a -c+ f+ -a ++f -b d -f +e -g+ +d -e \
    |21 g5 -c+ e -g +f+ -a+ +e -f+ ++a -d+ f+ --a ++b+ -f+ a -b+ \
    |22 *2 f6+ -a b+ -d+ * *2 f6+ -a b+ -d * \
    |23 f6+ -a c+ -c+ ++e -g+ c+ -c+ +c+ -e a -a +a -c+ f+ -f+ \
    |24 e5 -g+ c+ -c+ ++d -f+ a -d +c+ -e a -a ++b -d g -b \
    |25 *2 a4 -a c+ -c+ * g4+ -a c+ -c+ ++f+ -a c+ -c+ \
    |26 *2 f4+ -g+ c+ -c+ * *2 e4+ -g+ c+ -c+ * \
    |27 *4 a4 -c+ f+ -f+ * \
    |28 *4 f4+ -f+ b -b * \
    |29 *4 a4+ -c+ f+ -f+ * \
    |30 *4 f4+ -f+ b -b * \
    |31 *4 a4+ -c+ f+ -f+ * \
    |32 *4 a4 -c+ f+ -f+ * \
    |33 1/2 [a3 +e a] 1/4 [g -b] [c+ +g+] \
    |34 1/1 . \
    |35 \
').tag('bass')

################ VOLUME #################
#
# volume control has 3 layers:
# accent patterns (separate for LH, RH)
# vmeas: continuous change within measures
# vphrase: continuous change at 1-8 measure level

# RH accents
rha = '*4 .14 1/32 .1 1/32 .05 1/32 0 1/32 .05 1/32 0 1/32 .1 1/32 .07 1/32 *'

rh_accents = accents(f'meas4/4 \
    |1 *32 {rha} * \
    |33 \
')

lh_accents = accents('meas4/4 \
    |1 *32 \
        *4 .12 1/24 0 1/24 0 1/24 .12 1/8 * \
        * \
    |33 \
')

# swell to 4th beat
vm_4_sm = '[ 0 3/4 .07 1/4 0'
# bigger swell
vm_4_med = '[ 0 3/4 0.10 1/4 0'
# even bigger
vm_4_lg = '[ 0 3/4 0.13 1/4 0'
# swells to 2nd and 4th beat
vm_24 = '[ *2 0 1/4 .08 1/4 0 *'
# swell to 3rd beat
vm_3 = '[ 0 2/4 .1 2/4 0'

vmeas = vol(f'meas4/4 \
    |1 {vm_4_sm} {vm_4_med} {vm_24} {vm_3} \
    |5 {vm_4_med} {vm_4_lg} {vm_24} {vm_3} \
    |9 {vm_3} {vm_3} {vm_24} {vm_3} \
    |13 {vm_24} {vm_4_med} \
    |15 *4 {vm_4_med} * \
    |19 {vm_4_med} {vm_4_lg} {vm_24} {vm_24} \
    |23 *4 {vm_3} * \
    |27 *2 {vm_3} {vm_4_med} * \
    |31 *2 {vm_24} * \
    |33 *2 [ 0 1/1 0 * \
')

vphrase = vol('meas4/4 \
    |1 ppp 8/1 ppp \
    |9 ppp 4/1 f 2/1 _ff 2/1 _ff \
    |17 [ p 3/1 p \
    |20 p 2/1 ff 1/1 ff \
    |23 ff 4/1 p 2/1 p \
    |29 [ pp 2/1 pp \
    |31 exp5.0 pp 1/1 ff exp-5 1/1 pp linear \
    |33 [ mp 2/1 p \
    |35 \
')

################ TIMING #################
#
# timing control has 3 layers:
# pauses
# tbeat: accelerando within each beat
#    not sure if this is important, but the idea is
#    to create a feeling of always surging forward
# tphrase: tempo at phrase level
# currently this is common between LH and RH;
# it might be interesting to decouple at the tphrase level

# pause durations
dt0 = .02
dt1 = .04
dt2 = .06
dt3 = .08
dt4 = .10
dt5 = .12
dt6 = .15

# pause patterns for the 8 32ths in one beat
# 0 melody
# 1 melody octave
# 2
# 3
# 4
# 5
# 6 melody
# 7 melody octave

# Go lightly with pauses, else they affect tempo

# beat-level pauses
# default: short pauses after melody notes
pb0 = f'p{dt1} 1/32 . p{dt0} 5/32 . p{dt0} 1/32 . p{dt0} 1/32 .'
# phrase start: longer pause on 1st melody note
pb_start = f'p{dt5} 1/32 . p{dt0} 5/32 . p{dt0} 1/32 . p{dt0} 1/32 .'
pb_start_short = f'p{dt2} 1/32 . p{dt0} 5/32 . p{dt0} 1/32 . p{dt0} 1/32 .'
# phrase end: longer pause after last note
pb_end = f'p{dt1} 1/32 . p{dt0} 5/32 . p{dt0} 1/32 . p{dt3} 1/32 .'
# phrase end with shorter pause at end
pb_end_short = f'p{dt1} 1/32 . p{dt0} 5/32 . p{dt0} 1/32 . p{dt2} 1/32 .'

# measure 1 has a big pause after 1st note
pm1 = f'{pb_start} {pb0} {pb_start_short} {pb_end}'

# measure 2 has a lesser pause
pm2 = f'{pb0} {pb0} {pb_start} {pb_end}'

# measure 3: 2+2 beats
pm3 = f'{pb0} {pb_end} {pb0} {pb_end}'

# measure 8: moving forward, part of longer phrase
pm8 = f'{pb_start_short} {pb0} {pb0} {pb_end_short}'

pauses = tempo(f'meas4/4 \
    |1 {pm1} {pm2} {pm3} {pm2} \
    |5 {pm1} {pm2} {pm3} {pm8} \
    |9 *4 {pm8} * \
    |13 {dt2}p *4 {pm8} * \
    |17 {dt3}p *2 {pm8} * \
    |19 {pm1} {pm2} {pm3} {pm8} \
    |23 {dt3}p {pm8} {dt1}p {pm8} \
    |25 {dt1}p *2 {pm8} * \
    |27 {dt2}p *2 {pm8} * \
    |29 {dt2}p *2 {pm8} * \
    |31 {pm8} {dt4}p {pm8} {dt6}p \
    |33 \
')

# accel within each beat
tbeat = tempo('meas4/4 \
    |1 *32 *4 55 1/4 65 * * \
')

# accel mid-measure, rit at end
t1 = ' 40 2/4 60 2/4 40'

# more angst
t2 = ' 50 3/4 65 50 1/4 40'

# two 2-beat surges
t3 = '50 1/4 60 1/4 45 1/4 60 1/4 45'

# rit over 1 measure (phrase end)
trit = 'exp0.5 60 1/1 40 linear'

# accel mid-measure
t7 = '50 2/4 70 2/4 50'

# bigger rit
trit2 = '60 1/1 40'
 
# faster version of t1
t19 = '50 2/4 80 2/4 50'

tphrase = tempo(f'meas4/4 \
    |1 {t1} {t2} {t3} {trit} \
    |5 {t1} {t1} {t7} {t7} \
    |9 {t7} {t7} {t3} {t1} \
    |13 {t3} {t1} \
    |15 {t7} {t1} {t7} {trit2} \
    |19 *3 {t19} * 65 1/1 50 \
    |23 55 2/1 45 \
    |25 55 2/1 40 \
    |27 {t1} {trit} {t1} {trit2} \
    |31 50 1/1 70 60 1/1 45 \
    |33 40 2/1 30 \
    |35 \
')
    
# RH: pedal dotted 8th and 16th separately
rh_ped = pedal('meas4/4 \
    |1 *32 \
        + *4 3/16 1/16 * \
        * \
    |33 \
')
# LH: pedal the whole beat
lh_ped = pedal('meas4/4 \
    |1 *32 \
        + *4 1/4 * \
        * \
    |33 \
')

nuance = True

def main():
    ns = Score(tempo=90, verbose=False)
    if nuance:
        soprano.vsustain_pft(rh_ped)
        bass.vsustain_pft(lh_ped)
    ns.append_score([
        soprano,
        bass
    ])
    if nuance:
        ns.vol_adjust_pft(vphrase)
        ns.vol_adjust_pft(vmeas, mode=VOL_ADD)
        ns.vol_adjust_pft(rh_accents, pred=lambda n: 'soprano' in n.tags, mode=VOL_ADD)
        ns.vol_adjust_pft(lh_accents, pred=lambda n: 'bass' in n.tags, mode=VOL_ADD)
        #ns.tempo_adjust_pft(tbeat)
        ns.tempo_adjust_pft(tphrase)
        ns.tempo_adjust_pft(pauses)
        ns.roll(33/1+1/4, [0, .1, .2, .3, .5])
        ns.perf_dur_abs(1.9, lambda n: 'grace' in n.tags)
    #ns.trim(0, 4/1)
    #print(ns)
    fname = 'data/chopin_prelude_8.midi'
    preset = 'NY Steinway D Classical'
    ns.write_midi(fname)
    numula.pianoteq_rpc.loadMidiFile(fname)
    numula.pianoteq_rpc.midiPlay()
    #numula.pianoteq.play(fname, preset)

main()
