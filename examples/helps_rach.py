# Robert Helps: Hommage a Rachmaninoff

from numula.nscore import *
from numula.notate_score import *
import numula.pianoteq

sop = n('meas4/4 \
    |1 par-12 1/2 c+7 1/4 b d 1/2 c+ 1/4 b d+ \
    |3 c+ f+ e d c+ b a g \
    |5 1/2 f+ 1/4 e g 1/2 f+ 1/4 e g+ \
    |7 f+ b a +d c f e a \
    |9 *2 1/2 g+ 1/4 f+ a * \
    |11 meas6/4 g+7 1/8 a g+ g+ f+ e d+ f+ e d c+ \
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
sop.tag('sop')

alto = n('meas4/4 \
    |1 1/32 *36 f+6 g+ * *7 a b * a g+ *4 f+ g+ * \
    |4 *3 f+ g+ * f+ e *7 d e * d c+ *36 b c+ * \
    |7 *4 b c+ * *8 d e * *3 f g- * f g \
    |8 *4 f g * *7 a b- * a b *3 c+ d * c+ d+ \
    |9 *15 c+ d+ * c+ d *15 c+ d * c+ d+ \
    |11 meas6/4 1/32 c+7 d+ *6 c+ d * *4 c+ d+ * *4 c+ d * c+ b *8 a b * \
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

tenor = n('meas4/4 \
    |1 1/8 f+3 +c+ +b 1/4 c+ 1/8 -f+ +e +b \
    |2 f+3 +c+ +c+ 1/4 e+ 1/8 d+ +a g+ \
    |3 b -e -a b 1/4 c+ 1/8 -f+ g+ 1/4 a+ 1/8 c+ d 1/4 e 1/8 -a b \
    |5 3/8 c+ 1/4 d+ 1/8 c+ d+ -e \
    |6 +e d -f+ 1/4 +e+ 1/8 e f+ 1/4 e+ 1/8 e b c+ +f+ 1/4 f 1/8 g \
    |8 a -d a b 1/4 c+ 1/8 +c+ d+ \
    |9 c+2 ++g+ +f+ 1/4 +c+ 1/8 +c+ +a d \
    |10 b c+3 +g+ 1/4 +f+ 1/8 c+ ++d d+ \
    |11 meas6/4 1/4 e+ 1/8 d+ e+ 1/4 f+ 1/8 -a b 1/4 e 1/8 -g b- \
    |12 meas4/4 1/8 a4 f2 +f +c +a- c +g a- \
    |13 b-3 +f +e- 1/4 d- 1/8 b- +f e- \
    |14 b-3 +f +d c c b- f c \
    |15 b-3 +f +e- c --b- +f +d c \
    |16 --b- +f +d- c- c+3 ++e+ +b +g \
    |17 f+2 c+4 +b 1/4 +f+ 1/8 e g+ -g+ \
    |18 f+3 +c+ +a+ 1/4 +e+ 1/8 d+ +a+ 1/4 g+ 3/8 g+ 1/4 -a 1/8 . f \
    |20 g2 ++d +a 1/4 +f+ 1/8 e +b a \
    |21 1/4 [a -b] 1/8 -d 1/4 ++f+ 1/8 e f+ g \
    |22 1/4 [a -b] 1/8 . a 1/4 [g+ +d+] d+ \
    |23 [d- -e-] [+g- c-] [e- --d-] +b- \
    |24 1/8 . b-3 +f 1/4 +f +b- 1/8 -b- \
    |25 e-3 +b- +g 1/4 +e c+ 1/8 _ +g+ f+ \
    |26 . f+4 +e d . -d ++e d \
    |27 c+3 +g+ +g+ 1/4 +e 1/8 d e --d \
    |28 f+2 +f+ +c+ 1/4 +a 1/8 -d g+ f+ \
    |29 a+ --f+ +e 1/4 +d 1/8 -f+ +c+ b \
    |30 a+ --f+ +c+ 1/4 ++d+ 1/8 -g+ a+ 1/4 e+ \
        1/8 -f+ +c+ 1/4 +b 1/8 f+ +e d \
    |32 --f+ +c+ +b +b 1/2 ++c+ \
    |33 \
')
tenor.tag('tenor')

bass = n('meas4/4 \
    |1 4/4 . . 5/8 . 3/8 b3 1/8 c+ ++d+ 3/8 . 1/4 -e 1/8 . \
    |5 1/8 . b2 +f+ 5/8 . 4/4 . \
    |7 3/4 . 1/8 b-4 . 5/8 . 1/8 b3 1/4 -f+ \
    |9 7/4 . 1/4 a4 \
    |11 meas6/4 1/8 b4 -c+ 1/4 +c+ 1/8 b --b . . f+4 --e . . \
    |12 meas4/4 6/4 . 1/2 g-4 . g 16/4 . \
    |19 1/4 . 1/8 a+4 c 1/4 d 1/8 _ 3/8 g3 1/4 _ -c \
    |20 3/4 . 1/4 c5 1/8 . g3 1/4 . a4 c \
    |22 1/8 . d5 1/4 e 1/8 . 1/4 c+4 1/8 d+ \
    |23 1/8 . a-3 . c- . 3/8 a- 1/8 _ b- \
    |24 4/4 e-2 1/2 _ 1/4 c5 . \
    |25 1/2 . f+4 1/8 _ b \
    |26 1/2 b3 g 24/4 . \
    |33 \
')
bass.tag('bass')

# overall volume, 4-16 m scale

def main():
    ns = Score(tempo=80)
    ns.append_score([sop, alto, tenor, bass])
    ns.write_midi('data/helps_rach.midi')
    numula.pianoteq.play('data/helps_rach.midi')

main()
