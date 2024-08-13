# Robert Helps: Hommage a Rachmaninoff

from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

soprano = sh_score('meas4/4 \
    |1 par-12 1/2 c7+ 1/4 b d 1/2 c+ 1/4 b d+ \
    |3 c+ f+ e d c+ b a g \
    |5 1/2 f+ 1/4 e g 1/2 f+ 1/4 e g+ \
    |7 f+ b a +d c f e a \
    |9 *2 1/2 g+ 1/4 f+ a * \
    |11 meas6/4 g7+ 1/8 a g+ g+ f+ e d+ f+ e d c+ \
    |12 meas4/4 1/8 e7 d 11/16 c 1/16 a- \
    |13 1/2 f 1/4 e- g- 1/2 f 1/4 e- g 1/2 f f f f \
    |17 1/2 +c+ 1/4 d b 1/2 c+ 1/4 d+ b c+ +f+ f e- \
    |20 1/2 d 1/4 c e 1/2 d 1/4 e- c \
    |22 d +g f+ e e- e- d- c- \
    |24 1/2 b- 1/4 a- c 1/2 b- 1/4 a+ 1/8 b c+ \
    |26 1/4 c+ b a g 1/2 f 1/4 f 1/8 f+ g+ \
    |28 1/2 *7 f+ * 6/4 f+ \
    |33 par \
')
soprano.tag('sop')

alto = sh_score('meas4/4 \
    |1 1/32 *36 f6+ g+ * *7 a b * a g+ *4 f+ g+ * \
    |4 *3 f+ g+ * f+ e *7 d e * d c+ *36 b c+ * \
    |7 *4 b c+ * *8 d e * *3 f g- * f g \
    |8 *4 f g * *7 a b- * a b *3 c+ d * c+ d+ \
    |9 *15 c+ d+ * c+ d *15 c+ d * c+ d+ \
    |11 meas6/4 1/32 c7+ d+ *6 c+ d * *4 c+ d+ * *4 c+ d * c+ b *8 a b * \
    |12 meas4/4 1/32 *3 a6 b * a g *10 g a * g f e- d- *16 c d- * \
    |14 *32 c d * *15 c d * e f \
    |17 *32 f+ g+ * \
    |19 *4 f+ g+ * *4 a+ b * *3 b- c- * b- a *3 g a * g 2/32 a 1/32 a *15 g a * \
    |21 *16 g a * \
    |22 *4 g a * *7 b c * b a+ *4 g+ a * \
    |23 *16 a- b- * \
    |24 a- g *6 f g * f 2/32 g 1/32 g *7 f g * \
    |25 a- g *7 f g * g+ f+ *7 e f+ * \
    |26 *8 e f+ * *8 e d * *16 e d * \
    |28 *7 d c+ * d 2/32 c+ 1/32 b *3 c+ b * *4 e d * \
    |29 *7 d+ c+ * d+ 2/32 c+ 1/32 b *3 c+ b * *3 +e+ d+ * e+ 2/32 d+ \
         1/32 c+ *6 d+ c+ * d 2/32 c+ 1/32 c+ *6 d+ c+ * d+ 2/32 c+ \
         1/32 c+ *14 d c+ * d 33/32 c+ \
    |33 \
')
alto.tag('alto')

tenor = sh_score('meas4/4 \
    |1 1/8 f3+ +c+ +b 1/4 c+ 1/8 -f+ +e +b \
    |2 f3+ +c+ +c+ 1/4 e+ 1/8 d+ +a g+ \
    |3 b -e -a b 1/4 c+ 1/8 -f+ g+ 1/4 a+ 1/8 c+ d 1/4 e 1/8 -a b \
    |5 3/8 c+ 1/4 d+ 1/8 c+ d+ -e \
    |6 +e d -f+ 1/4 +e+ 1/8 e f+ 1/4 e+ 1/8 e b c+ +f+ 1/4 f 1/8 g \
    |8 a -d a b 1/4 c+ 1/8 -c+ d+ \
    |9 c2+ g3+ +f+ 1/4 +c+ 1/8 -c+ +a d \
    |10 b c3+ +g+ 1/4 +f+ 1/8 c+ ++d d+ \
    |11 meas6/4 1/4 e+ 1/8 d+ e+ 1/4 f+ 1/8 -a b 1/4 e 1/8 -g b- \
    |12 meas4/4 1/8 a4 f2 +f +c +a- c +g a- \
    |13 b3- +f +e- 1/4 d- 1/8 b- +f e- \
    |14 b3- +f +d c c b- f c \
    |15 b3- +f +e- c --b- +f +d c \
    |16 --b- +f +d- c- c3+ ++e+ +b +g \
    |17 f2+ c4+ +b 1/4 +f+ 1/8 e g+ -g+ \
    |18 f3+ +c+ +a+ 1/4 +e+ 1/8 d+ +a+ 1/4 g+ 3/8 g+ 1/4 -a 1/8 . f \
    |20 g2 ++d +a 1/4 +f+ 1/8 e +b a \
    |21 1/4 [a -b] 1/8 -d 1/4 ++f+ 1/8 e f+ g \
    |22 1/4 [a -b] 1/8 . a 1/4 [g+ +d+] d+ \
    |23 [d- -e-] [+g- c-] [e- --d-] +b- \
    |24 1/8 . b3- +f 1/4 +f +b- 1/8 -b- \
    |25 e3- +b- +g 1/4 +e c+ 1/8 _ +g+ f+ \
    |26 . f4+ +e d . -d ++e d \
    |27 c3+ +g+ +g+ 1/4 +e 1/8 d e --d \
    |28 f2+ +f+ +c+ 1/4 +a 1/8 -d g+ f+ \
    |29 a+ --f+ +e 1/4 +d 1/8 -f+ +c+ b \
    |30 a+ --f+ +c+ 1/4 ++d+ 1/8 -g+ a+ 1/4 e+ \
        1/8 -f+ +c+ 1/4 +b 1/8 f+ +e d \
    |32 --f+ +c+ +b +b 1/2 ++c+ \
    |33 \
')
tenor.tag('tenor')

bass = sh_score('meas4/4 \
    |1 4/4 . . 5/8 . 3/8 b3 1/8 c+ ++d+ 3/8 . 1/4 -e 1/8 . \
    |5 1/8 . b2 +f+ 5/8 . 4/4 . \
    |7 3/4 . 1/8 b4- . 5/8 . 1/8 b3 1/4 -f+ \
    |9 7/4 . 1/4 a4 \
    |11 meas6/4 1/8 b4 -c+ 1/4 +c+ 1/8 b --b . . f4+ --e . . \
    |12 meas4/4 6/4 . 1/2 g4- . g 16/4 . \
    |19 1/4 . 1/8 a4+ c 1/4 d 1/8 _ 3/8 g3 1/4 _ -c \
    |20 3/4 . 1/4 c5 1/8 . g3 1/4 . a4 c \
    |22 1/8 . d5 1/4 e 1/8 . 1/4 c4+ 1/8 d+ \
    |23 1/8 . a3- . c- . 3/8 a- 1/8 _ b- \
    |24 4/4 e2- 1/2 _ 1/4 c5 . \
    |25 1/2 . f4+ 1/8 _ b \
    |26 1/2 b3 g 24/4 . \
    |33 \
')
bass.tag('bass')

soprano_v0 = sh_accents('meas4/4 \
    |1 *10 1.2 1/4 1.1 1/4 1.1 1/4 1 1/4 * \
    |11 meas6/4 *3 1.2 1/4 1.1 1/4 * \
    |12 meas4/4 *21 1.2 1/4 1.1 1/4 1.1 1/4 1 1/4 * \
    |33 \
')

# 130 beats, 65 half-notes
# each half note (16 32nd notes) has the following accent pattern:
#####
#
##
#
###
#
##
#
####
#
##
#
###
#
##
#

a5 = 1.2
a4 = 1.1
a3 = 1.05
a2 = 1.0
a1 = .9

alto_v0 = sh_accents(f' \
    *65 {a5} 1/32 {a1} 1/32 {a2} 1/32 {a1} 1/32 \
      {a3} 1/32 {a1} 1/32 {a2} 1/32 {a1} 1/32 \
      {a4} 1/32 {a1} 1/32 {a2} 1/32 {a1} 1/32 \
      {a3} 1/32 {a1} 1/32 {a2} 1/32 {a1} 1/32 \
    * \
')

alto_v1 = sh_vol('meas4/4 \
    |1 *2 *2 pp 2/4 mp 2/4 pp * pp 4/4 mp 4/4 pp * \
    |9 *2 pp 2/4 mp 2/4 pp * \
    |11 meas6/4 pp 6/4 pp \
    |12 meas4/4 pp 84/4 pp \
    |33 \
')

tenor_v0 = sh_vol('meas4/4 \
    |1 mp 10/1 mp \
    |11 meas6/4 mp 6/4 mp \
    |12 meas4/4 mp 84/4 mp \
    |33 \
')

tenor_v1 = sh_vol('meas4/4 \
    |1 -1 9/4 -1 \
        *4 [ p 1/4 mp [ mp_ 1/4 mp_ * \
        ] -1 3/4 -1 \
    |6 \
')

bass_v0 = sh_vol('meas4/4 \
    p 44/4 p \
    |11 meas6/4 p 6/4 p \
    |12 meas4/4 p 12/1 p \
    |24 [ f 4/4 f [ p 8/1 p \
    |33 \
')
# overall volume, 4-16 m scale
v0 = sh_vol('meas4/4 \
    |1 p 6/4 p 2/4 pp 8/4 p 16/4 mf 8/4 f \
    |11 meas6/4 f 6/4 f \
    |12 meas4/4 f 1/4 ff 3/4 mp 4/4 mp \
    |14 [ p 12/4 pp \
    |17 pp 4/4 p 8/4 f \
    |20 f 16/4 _f 4/4 mf \
    |25 mf 2/4 p 10/4 pp \
    |28 pp 16/4 ppp 4/4 ppp \
    |33 \
')

# tempo
t0 = sh_tempo('meas4/4 \
    |1 *2 55 2/4 65 2/4 60 60 2/4 65 2/4 60 65 8/4 55 * \
    |9 60 2/4 65 2/4 60 60 2/4 65 2/4 60 \
    |11 meas6/4 65 6/4 60 \
    |12 meas4/4 60 4/4 45 \
    |13 60 4/4 60 55 4/4 55 60 8/4 50 \
    |17 *2 *2 60 2/4 65 2/4 60 * 60 4/4 55 * \
    |23 55 4/4 50 \
    |24 60 4/4 65 65 12/4 55 \
    |28 60 8/4 55 8/4 50 4/4 15 \
')

# pause durations
dt0 = .03
dt1 = .05
dt2 = .08
dt3 = .11
dt4 = .14

# pauses
t1 = sh_tempo(f'meas4/4 \
    |1 *2 {dt2}p 4/4 . {dt1}p 4/4 . \
        {dt1}p 8/4 . \
        * \
    |9 {dt2}p 4/4 . {dt1}p 4/4 . \
    |11 meas6/4 {dt2}p 6/4 . \
    |12 meas4/4 {dt1}p 1/4 . {dt2}p 3/4 . \
    |13 *2 {dt2}p 4/4 . * 8/4 . \
    |17 {dt3}p 4/4 . {dt1}p 8/4 . \
    |20 {dt2}p 4/4 . {dt1}p 12/4 . \
    |24 {dt2}p 4/4 . {dt1}p 4/4 . \
    |26 {dt0}p 4/4 . {dt1}p 4/4 . \
    |28 *4 {dt1}p 4/4 . * {dt4}p{dt4} 4/4 . \
    |33 \
')

# pedal over measures
mped = sh_pedal('meas4/4 \
    |1 *10 + 4/4 * \
    |11 meas6/4 + 6/4 \
    |12 meas4/4 *21 + 4/4 * \
    |33 \
')

nuance = True

def main():
    ns = Score(tempo=80, verbose=False)
    if nuance:
        soprano.vol_adjust(.7, lambda n: 'bottom' in n.tags)
        soprano.vol_adjust_pft(soprano_v0)
        alto.vol_adjust_pft(alto_v0)
        alto.vol_adjust_pft(alto_v1)
        tenor.vol_adjust_pft(tenor_v0)
        bass.vol_adjust_pft(bass_v0)
    ns.append_score([
        soprano,
        alto,
        tenor,
        bass
    ])
    if nuance:
        ns.vsustain_pft(mped, 0, lambda n: 'alto' in n.tags)
        ns.vsustain_pft(mped, 0, lambda n: 'tenor' in n.tags)
        ns.vsustain_pft(mped, 0, lambda n: 'bass' in n.tags)
        ns.vol_adjust_pft(v0)
        tenor.vol_adjust_pft(
            tenor_v1, pred=lambda n: 'tenor' in n.tags, mode=VOL_SET
        )
        ns.tempo_adjust_pft(t0)
        ns.tempo_adjust_pft(t1)
    #print(ns)
    ns.write_midi('data/helps_rach.midi')
    numula.pianoteq.play('data/helps_rach.midi')

main()
