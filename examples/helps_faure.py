# Robert Helps: Hommage a Faure

from numula.nscore import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

# rhythmic patterns used in the melody (soprano)
#
r1 = '<1/2 1/4 1/4 3/4 1/4 1/4 1/4 1/4 1/4 4/4>'
r2 = '<1/2 1/4 1/4 2/4 1/4 1/4 1/4 1/4 1/4 1/4 4/4>'

soprano = n(f'meas4/4 \
    |1 {r1} b-6 a- b- c- b- b- a- g- a- b- \
    |5 {r2} g- f g- b- a- g- g- f e- f g- \
    |9 {r1} b-6 a- b- c- b- b- a- g- a- b- \
    |13 g- f g- b- a- g- f c d e- \
    |17 +b- a- b- c- b- b- a- g- a- b- \
    |21 {r2} g- f g- b- a- g- g- f e- f g- \
    |25 {r1} b- a- b- c- b- b- a- g- a- b- \
    |29 {r2} g- f g- b- a- g- g- f c d \
    |32 meas2/4 1/2 e- \
    |33 meas4/4 {r1} +b- a- b- c- b- b- a- g- a- b- \
    |37 1/2 g-5 1/4 f g- 1/2 b- 1/4 +a- --g- +g- f e- f \
    |40 meas2/4 g- f \
    |41 meas4/4 {r1} b- a- b- c- b- b- g+ g- a- b- \
    |45 g- f g- 1/2 b- . 4/4 . . . \
    |50 meas2/4 2/4 . \
    |51 meas4/4 {r1} b-5 a b- c- b- b- a- g- a- b- \
    |55 {r2} g- f g- b- a- g- g- f e- f g- \
    |59 {r1} b- a b- c- b- b- a- g- a- b- \
    |63 g- f g- b- a- g- f c d 4/4 e- \
    |67 \
').tag('sop')

alto = n('meas4/4 \
    |1 1/4 . [a-5 d-] . [d- e-] . [c- d-] . d- \
    |3 . [c- d-] . [c- d-] . [a- d-] . [e- f] \
    |5 . [-a- g-] . +d- . [d- c-] . d- \
    |7 . -g- . b- . [d- -g-] . . \
    |9 . [a- d-] . d . [d- c-] . c- \
    |11 . [c- d-] . c- . [d- a-] . [b- +f] \
    |13 . [-a- g-] . a- . [a- d-] . d- \
    |15 . c . c 4/4 . \
    |17 1/12 b-6 -b- d- +b- b- +b- --a- -b- d- +b- b- +b- \
    |18 -c- -c- d- g- c- d- +c- g- d- b- -d- c- \
    |19 +b- -c- d- +a- d- +d- --g- -c- d- +a- d- +d- \
    |20 --b- -b- d- +a- b- d- +b- a- e- b- a- -d- \
    |21 g- -g- b- +g- +f -b- f -b- +b- g- +e- --d- \
    |22 +b- -c- d- g- ++b- -d- a- -c- d- g- +g- -b- \
    |23 g- -a- b- +f b- +b- --e- -a- ++b- f c +c \
    |24 -g- d- +d- c b- a- f e- d- c b- f \
    |25 ++b- -b- d- +a- b- +b- --a- -b- d- +b- b- +b- \
    |26 -c- -c- d- g- c- d- +c- b- -d- b- -d- c- \
    |27 +b- -c- d- +a- d- +d- --g- -c- d- +a- d- +d- \
    |28 --b- -b- d- +a- b- d- +b- a- g- e- -a- -d- \
    |29 g- -g- b- +f g- +f -f b- -b- +g- d- ++e- \
    |30 b- -c- d- g- +d- +d- --a- -c- d- g- ++b- -d- \
    |31 -g- -a- b- +f +c -c c -f b- d +c -c \
    |32 meas2/4 e- -f b- d +c -c \
    |33 meas4/4 1/16 +b- a- e- -a- b- d- e- a- ++b- a- -d- a- b- a- -e -g \
    |34 +d- c- b- c- d- e- g- +d- +c- b- -e- b- b- a- -d -f+ \
    |35 +d c- b- c- d- +c- [e- +c] --b- -d- c- a- b- d g- [+d- +c-] -c- \
    |36 -d- c -f a- b- d- e- a- ++b- a- [c- -e-] d- [f- -a-] g- [+c- -e-] d- \
    |37 [e- +b-] -d- b- c- [d- g-] a- [b- e-] f \
        [e- +b-] -d- [g- -b-] a- [a- +f] -g- [f +d-] -e- \
    |38 +b- a- e- -a- b- d- e- a- ++b- a- -d- b- d- a- -d- b- \
    |39 +g- -a- g- a- +f b- +b- -b- -e- -a- g- a- +f b- +b- -b- \
    |40 meas2/4 -b- a- g- a- b- +b- [+f b-] -b- \
    |41 meas4/4 -e- d- a- d- e f+ b c+ +b b- -f- -a- b- g- e -g \
    |42 +f- e- c- d- g- a- b- d- +b- a- [c- -e-] d- f -a- +f+ --f \
    |43 e d b c+ e +b [c+ +b] -b -d- c- a- b- d- +c- [d- +c-] -c- \
    |44 -d- c- a- c- d- e- a- a- ++c- b- g- d- e -a -d -g \
    |45 b- a- f g- c- d- f g- [+e- +c] -d- g- -b- -b- a- +d- -g- \
    |46 ++b- a- e- -a- d- e- g- +d- +d- b- -e- d- b- a- -d- a- \
    |47 ++b- a- g- -b- +g- f -c- -f ++b- a- -d- -g- +f -c- a f \
    |48 ++b- a- -d- -g- +g- f -c- -f ++b- a- f- -b- +f -c- a f \
    |49 +f e- -a f b- e- f ++g- d- -a -d- -a +a -e- -a -d- \
    |50 meas2/4 ++d- -a -d- -a +a -e- -a -d- \
    |51 meas4/4 \
')

bass = n('meas4/4 \
    |1 1/8 f5 -b- d- -e- ++a- 1/4 -d- 1/8 _ e- -e- \
    |2 -a- +g- +d- c- +g- d- e- -g- \
    |3 +g- -c- e- --d- ++g- 1/4 -c- 1/8 _ d- -d- \
    |4 ++a- -b- d- -e- ++a- 1/4 e- 1/8 _ g d- \
    |5 b- -c- ++d- a- +f -b- e- -g- \
    |6 g- -a- ++d- -g- ++a- -c- e- -a- \
    |7 c- --b- +a- c- +g- -c- e- 1/4 -a- 1/8 e- +b- d- f e- +b- -e- \
    |9 a- -d- b- +b- a- -d- d -e \
    |10 e -a- +e- +d- g- -c- d- -g- \
    |11 +g- -c- e- --d- ++g- 1/4 -c- 1/8 _ d --d- \
    |12 +b- -e- ++f d- +a- 1/4 -d- 1/8 _ e- -g \
    |13 b- a- d- --c- ++f -b- e- -g- \
    |14 e- -a- +g- +d- +c- -e- g- -b- \
    |15 a- -b- ++c d +b- -c +g -a- \
    |16 a- -b- +g- b- +f e- d- a- \
    |17 e- +b- +f d- +b- -e- a- -d- \
    |18 --a- +e- +c- +g- +d- -d- e- -g- \
    |19 d- +c- +f +c- -e- d- f -c- \
    |20 g-3 +f b- +f 1/4 d- 1/8 _ e- b- -f- \
    |21 -c- +g- +e- b- +f -a- d- -g- \
    |22 -a- +g- +d- +a- -c- d- +c- --a- \
    |23 -b- +a- +d g- -c- a- 1/4 +d \
    |24 1/8 -e- +b- +f d- +c -f e- d- \
    |25 f -b- d- -e- ++a- 1/4 -d- 1/8 _ _ e- g -g \
    |26 e- -a- +g- +d- +d- -e- d -g- \
    |27 d- +c- e- +b- g- -c- d- -d- \
    |28 -g- +f- +b- e- +b- -d- e- -f- \
    |29 +e- -g- -c- +b- +f -a- d- -g- \
    |30 e- -a- ++c- -g- +g- -c- d- -e- \
    |31 b- +a- +d c +b- -c d -f \
    |32 meas2/4 1/12 --e- +b- +f g- b- +f \
    |33 meas4/4 1/8 a- -d- -e- +b- ++a- -d- -g -d- \
    |34 g- -a- g- -a- e-6 -g- c- -d \
    |35 g-5 -c- c- -d- ++g- d- g- -c- \
    |36 +f -b- -e- +d- +a- d- a- -d- \
    |37 g- -c- -e- -a- ++f -a- +g- -c- \
    |38 +b- --f +c- e- ++a- e- -g- -c- \
    |39 e- -a- f -b- ++d -a- f -b- \
    |40 meas2/4 [+a- +e-] --b- [+a- +e-] -b- \
    |41 meas4/4 ++c- --e- [+b- d-] +d- 1/16 +a- g- e- d- -g f- e- d- \
    |42 +g- -a- c- g- +d- -e- g- -a- +e- g- c- e- +b- -d f -b \
    |43 1/12 +f -b d +b- -b d f -b d +b- -b d \
    |44 1/8 f d- -e- ++d- +d- -d- 1/4 g+ 1/8 _ -d \
    |45 1/16 d- -e- g- -a- ++c- d- +c- g- +f -c- b- a- f -c- b- a- \
    |46 1/8 +e- -f +c- +a- d- -e- g- -c- \
    |47 *2 g-5 -a- +d --b- ++e- -a- +d --b- * \
    |49 e- +b- 3/4 . \
    |50 meas2/4 2/4 . \
    |51 meas4/4 1/8 -e- g +d- 1/4 f- 1/8 e- d -e- \
    |52 -a- +f- +c- +f- d c+ b -e \
    |53 d- f +d b +b -d c 1/4 -f 1/8 _ \
    |54 -g- +f b- e- g -a- +f- -f- \
    |55 -c- +g- b- 1/4 e- 1/8 d- e- -a- \
    |56 -a- +e- g- 1/4 +d- 1/8 -e- ++a- -b- \
    |57 -b- +a- +e- +b- b- a -b a \
    |58 a b- +f- e- d a f -b- \
    |59 -e- ++f- g +d- +f+ e -g e \
    |60 -a- +e g +e d -f+ d -a- \
    |61 -d- ++f +b +e- +d- b -b g \
    |62 -g +e- +c b- +f e- d -d \
    |63 -a- +g- +c- -e- . e- +d- c- \
    |64 --f +c +c b- ++c -e- b- f \
    |65 -b- +a- a- ++c . --b- +g --f \
    |66 --e- +b- +b- g 1/2 +g \
    |67 \
')

soprano_v0 = vol('meas4/4 \
    |1 *7 p 1/1 mf 1/1 p 1/1 mp 1/1 p * \
    |29 p 2/1 mf 1/1 p \
    |32 meas2/4 p 2/4 pp \
    |33 meas4/4 [ p 1/1 mf 1/1 p 1/1 mp 1/1 p \
    |37 p 2/1 mf 1/1 mp \
    |40 meas2/4 mp 2/4 f \
    |41 meas4/4 f 1/1 mf 1/1 f 2/1 p \
    |45 p 5/1 pp \
    |50 meas2/4 pp 2/4 p \
    |51 meas4/4 p 1/1 mf 1/1 p 1/1 mp 1/1 pp \
    |55 [ p 1/1 mf 1/1 p 1/1 mp 1/1 mf \
    |59 mf 4/1 ppp \
    |63 [ p 4/1 ppp \
    |67 \
')
alto_v0 = vol('meas4/4 \
    |1 ppp 31/1 ppp \
    |32 meas2/4 [ ppp 2/4 ppp \
    |33 meas4/4 *7 ppp 2/4 pp 2/4 ppp * \
    |40 meas2/4 ppp 2/4 p \
    |41 meas4/4 p 1/1 pp 1/1 mp 2/1 ppp \
    |45 ppp 4/1 ppp \
    |49 ppp 2/4 p 2/4 ppp \
    |50 meas2/4 ppp 2/4 ppp \
    |51 meas4/4 \
')
bass_v0 = vol('meas4/4 \
    |1 *31 pp 2/4 p 2/4 pp * \
    |32 meas2/4 [ pp 2/4 pp \
    |33 meas4/4 *7 pp 2/4 p 2/4 pp * \
    |40 meas2/4 pp 2/4 pp \
    |41 meas4/4 *9 pp 2/4 p 2/4 pp * \
    |50 meas2/4 pp 2/4 pp \
    |51 meas4/4 [ ppp 4/1 ppp \
    |55 ppp 2/1 ppp 2/1 mf \
    |59 mf 4/1 ppp \
    |63 [ p 4/1 ppp \
    |67 \
')

bass_v1 = accents('meas4/4 \
    |1 *62 mm 1/8 p 1/8 mp 1/8 p 1/8 * \
')

# tempo
t0 = tempo('meas4/4 \
    |1 *3 \
        55 1/1 65 1/1 55 60 1/1 60 1/1 50 \
        * \
    |13 55 1/1 65 1/1 55 60 1/1 60 1/1 40 \
    |17 *3 \
        55 1/1 65 1/1 55 60 1/1 60 1/1 50 \
        * \
    |29 55 1/1 65 1/1 55 60 1/1 50 \
    |32 meas2/4 2/4 40 \
    |33 meas4/4 7/1 \
    |40 meas2/4 2/4 \
    |41 meas4/4 9/1 \
    |50 meas2/4 2/4 \
    |51 meas4/4 16/1 \
    |67 \
')

dt0 = .03
dt1 = .05
dt2 = .08
dt3 = .11
dt4 = .14

pauses = tempo(f'meas4/4 \
    |1 *7 \
        p{dt2} 1/1 . {dt1}p{dt2} 2/1 . {dt0}p 1/1 . \
        * \
    |29 p{dt2} 1/1 . {dt1}p{dt2} 2/1 . \
    |32 meas2/4 {dt0}p 2/4 . \
    |33 meas4/4 7/1 \
    |40 meas2/4 2/4 \
    |41 meas4/4 9/1 \
    |50 meas2/4 2/4 \
    |51 meas4/4 16/1 \
    |67 \
')

# agogic accents in melody

sop_shift = shift(f'meas4/4 \
    |1 *4 \
        {dt2} 1/1 {dt1} 1/1 1/1 {dt2} 1/1 \
        * \
    |17 \
    |32 meas2/4 {dt0}p 2/4 . \
    |33 meas4/4 7/1 \
    |40 meas2/4 2/4 \
    |41 meas4/4 9/1 \
    |50 meas2/4 2/4 \
    |51 meas4/4 16/1 \
    |67 \
')

bass_ped = pedal('meas4/4 \
    |1 *31 + 4/4 * \
    |33 meas4/4 7/1 \
    |40 meas2/4 2/4 \
    |41 meas4/4 9/1 \
    |50 meas2/4 2/4 \
    |51 meas4/4 16/1 \
    |67 \
')

nuance = True

def main():
    ns = Score(tempo=80)
    if nuance:
        soprano.vol_adjust_pft(soprano_v0)
        alto.vol_adjust_pft(alto_v0)
        bass.vol_adjust_pft(bass_v0)
        bass.vol_adjust_pft(bass_v1)
        bass.vsustain_pft(bass_ped)
    ns.append_score([
        soprano,
        alto,
        bass
    ])
    if nuance:
        ns.tempo_adjust_pft(t0)
        ns.tempo_adjust_pft(pauses)
        ns.time_shift_pft(sop_shift, pred=lambda n: 'sop' in n.tags)
    #print(ns)
    fname = 'data/helps_faure.midi'
    ns.write_midi(fname, verbose=False)
    numula.pianoteq.play(fname)


main()
