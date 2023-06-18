# Robert Helps: Hommage a Rachmaninoff

from numula.nscore import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

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
    |34 \
')
soprano.tag('sop')

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
    |34 \
')
bass.tag('bass')

# volume control has 3 layers:
# accent patterns (separate for LH, RH)
# vmeas: continuous change within measures
# vphrase: continuous change at 1-8 measure level

rh_accents = accents('meas4/4 \
    |1 *32 \
        *4 mf 1/32 mf_ 1/32 p 1/32 _p 1/32 p 1/32 _p 1/32 mf_ 1/32 mm 1/32 * \
        * \
    |33 \
')

lh_accents = accents('meas4/4 \
    |1 *32 \
        *4 mm 1/24 p 1/24 p 1/24 mp 1/8 * \
        * \
    |33 \
')

vmeas = vol('meas4/4 \
    |1 *2 mm 3/4 mf 1/4 mm * \
    |3 *2 mm 1/4 mf 1/4 mm * \
    |4 mm 2/4 mf 2/4 mm \
    |5 *28 mm 1/1 mm * \
    |33 *2 mm 1/1 mm * \
')

vphrase = vol('meas4/4 \
    |1 pp 8/1 pp \
    |9 pp 4/1 f 2/1 ff 2/1 ff \
    |17 [ p 3/1 p \
    |20 p 2/1 ff 1/1 ff \
    |23 ff 4/1 p 2/1 p \
    |29 [ pp 6/1 pp \
    |35 \
')

# timing control has 3 layers:
# pauses
# tmeas: tempo at beat level
# tphrase: tempo at phrase level
# currently this is common between LH and RH;
# it might be interesting to decouple at some level

# pause durations
dt0 = .02
dt1 = .04
dt2 = .06
dt3 = .08
dt4 = .10
dt5 = .12

# 'compound pauses' for pairs of melody notes
# (octaves in the 1st and 4th 16th of a beat)
p0 = f'{dt0}p 1/32 . p{dt0} 1/32 .'
p1 = f'{dt1}p 1/32 . p{dt1} 1/32 .'
p2 = f'{dt2}p 1/32 . p{dt2} 1/32 .'
p3 = f'{dt3}p 1/32 . p{dt3} 1/32 .'

# a measure like measure 1
pm1 = f'{p3} 1/8 . {p0} {p1} 1/8 . {p0} {p1} 1/8 . {p0} {p2} 1/8 . {p0}'

# measure 3: 2+2 beats
pm3 = f'*2 {p2} 1/8 . {p0} {p1} 1/8 . {p0} *'

# measure 8: moving forward, part of longer phrase
pm8 = f'{p2} 1/8 . {p0} *3 {p1} 1/8 . {p0} *'

pauses = tempo(f'meas4/4 \
    |1 {pm1} {pm1} {pm3} {pm8} \
    |5 {pm1} {pm1} {pm3} {pm8} \
    |9 *4 {pm8} * \
    |13 {dt2}p *4 {pm8} * \
    |17 {dt3}p *2 {pm8} * \
    |19 {pm1} {pm1} {pm3} {pm8} \
    |23 {dt3}p {pm8} {dt1}p {pm8} \
    |25 {dt1}p *2 {pm8} * \
    |27 {dt2}p *2 {pm8} * \
    |29 {dt2}p *2 {pm8} * \
    |31 {pm8} {dt2}p {pm8} \
    |33 \
')

# slight accel within each beat
tmeas = tempo('meas4/4 \
    |1 *32 *4 55 1/4 65 * * \
')

# slight accel mid-measure
t1 = '60 2/4 70 2/4 55'

# same, but less rit at end
t7 = '60 2/4 70 2/4 60'

# rit over 1 measure (phrase end)
trit = '60 1/1 45'

# bigger rit
trit2 = '60 1/1 40'

# faster version of t1
t19 = '65 2/4 75 2/4 60'

tphrase = tempo(f'meas4/4 \
    |1 *3 {t1} * {trit} \
    |5 {t1} {t1} *11 {t7} * {trit} \
    |19 *3 {t19} * 65 1/1 50 \
    |23 60 2/1 50 \
    |25 60 2/1 50 \
    |27 {t1} {trit} {t1} {trit2} \
    |31 60 1/1 70 1/1 50 \
    |33 50 2/1 40 \
    |35 \
')

# RH articulation: sustain melody notes
def rh_art(ns):
    ns.score_dur_abs(3/16, lambda n: n.time % (1/4) == 0)
    ns.score_dur_abs(5/32, lambda n: n.time % (1/4) == 1/32)
    ns.score_dur_abs(1/16, lambda n: n.time % (1/4) == 3/16)
    
# LH articulation: pedal each beat
lh_ped = pedal('meas4/4 \
    |1 *32 \
        + 1/4 1/4 1/4 1/4 \
        * \
    |33 \
')

nuance = True

def main():
    ns = Score(tempo=90, verbose=False)
    if nuance:
        #soprano.vol_adjust_pft(rh_accents)
        bass.vol_adjust_pft(lh_accents)
        rh_art(soprano)
        bass.vsustain_pft(lh_ped)
        
    ns.append_score([
        soprano,
        bass
    ])
    if nuance:
        ns.vol_adjust_pft(vmeas)
        ns.vol_adjust_pft(vphrase)
        ns.tempo_adjust_pft(tmeas)
        ns.tempo_adjust_pft(tphrase)
        ns.tempo_adjust_pft(pauses)
    #print(ns)
    ns.write_midi('data/chopin_prelude_8.midi')
    numula.pianoteq.play('data/chopin_prelude_8.midi')

main()
