# Beethoven sonata op 57, 3rd mvt

from note import *
from notate import *
from nuance import *
import pianoteq

def make_score():
    # measures 1-49
    rh_1_49 = n('1/16 \
        . *2 \
        *2 -c f a- c d- c b- | a- b- a- g f g a- f . * \
        d- g- b- d- e- d- c | b- c b- a- g- a- g- f \
        e f g e f g a- f | g a- b- g e f g e f * \
        |36 *2 #c5 c f a- c -c f a- . * \
        -b d +a- b -b d +a- b -b e g c -c e g \
        *3 . -c e g c -c e g * c -c e g c -c f a- \
        *3 . -f a c f -f a c * \
        [-f a] +f [-f b-] +f [-f +c] f [-f +d-] f \
        . --c f a- c -c f a- c -c +g b- c -c e g \
    ')
    lh_1_49 = n('*2 #f2 1/4 f . . 3/16 . 1/16 +f * \
        1/4 -b- . . 3/16 . 1/16 d- \
        1/8 c . d- . b- . c . \
        *2 #f2 1/4 [f +f] 3/16 . 1/16 #c6 [c -a-] 1/4 [c -a-] [a- f] * \
        #c3 1/4 [b- +b-] 3/16 . 1/16 #c6 [b- d-] 1/2 [b- d-] \
        1/8 [c b-] [--c -c] . [d- +d-] . [b- -b-] . [c +c] \
        |36 1/4 [--f +f] 3/16 . 1/16 [+f a-] 1/4 [a- f] 3/16 . 1/16 [a- f] \
        2/4 [a- f c] 1/8 [c e g] . 1/4 . [-c -c] 3/16 . 1/16 [++g b-] \
        1/4 [g b-] 3/16 . 1/16 [g b-] 2/4 [f g b-] \
        1/8 [f a-] . 1/4 . [f -f] 3/16 . 1/16 [++c e-] 1/4 [c e-] 3/16 . 1/16 [c e-] \
        |46 5/8 [b- c e-] 1/8 [d- b-] [c a-] [b- g] \
        1/4 [a- f c] 3/16 . 1/16 [f a-] 1/4 [b- g -c] 3/16 . 1/16 [e g] \
    ')
    # measures 50-117
    rh_50_117 = n(' \
        1/4 [c f a- c] 3/16 . 1/16 [f a-] 1/4 [f a-] 3/16 . 1/16 [f a-] \
        |52 1/2 [f a-] 1/8 [g e] 5/8 . 3/16 . 1/16 [g b-] 1/4 [g b-] \
        3/16 . 1/16 [g b-] 1/2 [g b-] 1/8 [a- f] 5/8 . 3/16 . 1/16 [+c e-] \
        1/4 [c e-] 3/16 . 1/16 [c e-] 5/8 [c e-] \
        1/8 [d- b-] [c a-] [b- g] 1/4 [f a-] \
        3/16 . 1/16 [f a- +f] 1/4 [g -b- g] 3/16 . 1/16 [e g +e] [f -a- f] \
        *2 c f a- c d- c b- a- b- a- g f g a- f . * \
        *2 f b d f g f e- d e- d c b c d b . * \
        *2 g c e- g a- g f e- f e- d c d e- c . * \
        *2 d- e- d- e- d- c d- . b c b . c d c . * \
        |80 d- e- d- e- d- c d \
        . b c b . a- b- a- . g a- g . f+ g f+ . f g f . e- f e- . \
        e- f e- . d e- d . c d c . b c b \
        . a- *3 +a- -a- * . a- +a- g f e- d c \
        . +a- *3 +a- -a- * . a- +a- g f e- d c \
        . --a- *3 +a- -a- * . +a- -a- +a- . +a- -a- +a- \
        . g -g +g . f+ -f+ +f+ . f -f +f . e- [-g e-] +e- \
        . e- [-a -e-] +e- . d [a -d] +d . c [-e- c] +c . b [-d b] +b [c g e- c] \
        g c e- g a- g f e- f e- d c b- a- g f e- d c 1/8 b \
        [g b d g] *4 [-g b +f g] * 1/16 [g e- c g] \
        ++g c e- g a- g f e- f e- d c b- a- g f e- d c 1/8 b \
        [g b d g] *4 [-g b +f g] * 1/4 [g e- c g] 1/8 . \
        [+g c e- g] *4 [-g b +f g] * 1/4 [g e- c g] 1/8 . \
        [-g c e- g] *4 [-g b +f g] * 1/4 [g e- c g] 1/8 . \
        [c e- g c] *4 [-c e g c] * 1/4 [c a- f c] 1/8 . \
        [-c f a- c] *4 [-c e +b- c] * \
        1/16 #c6 [c a -e- c] a c e- g- a c e- \
        g- a c e- g- e- c a g- e- c a g- e- c a \
        g- e- c a g- e- c a *4 -g- a c e- * \
    ')

    foo = n('1/8 b [g b d g] \
        |99 *4 [-g b +f g] * 1/4 [g e- c g] 1/8 . \
    ')
    lh_50_117 = n('1/16 -f +c a- f c +a- f c a- +f c a- f +c a- f \
        c f a- c b c b c b c g c -e +c g c \
        |54 -c e g c -e g c e -g c e g -c e g c \
        -f a- c f e f e f e f c f -a- +f c f \
        |58 -f a c f -a c f a -c f a c -f a c f \
        -a +f e f -a +f -a +f -a +f -b- +f c f d- f \
        |62 --c f a- c b c b c -c e g c -c +g b- c \
        *2 #f4 f [+f a-] *7 [c -c] [f a-] * * \
        *2 #g3 g [+f g] *3 [d +b] [g f] * *2 [d +b] [a- f] * *2 [d +b] [g f] * * \
        |72 -c [+c e-] *7 [g -g] [c e-] * \
        1/8 --c 1/16 ++g e- +c g c g +e- c e- c +g e- g e- \
        |76 *2 3/8 [f a-] 1/8 [g e-] 1/4 [f d] [e- g] * \
        |80 3/8 [f a-] 1/8 [g e-] 1/4 [f d] [e- c] [d b] [c a] [c a-] [c g] \
        2/4 f+ 1/4 _ a 2/4 [g -g] 1/4 _ _ +e- d \
        |86 *2 3/8 [d- a- f] 1/8 [e- g c] 1/4 [b f d] [e- g c] * \
        3/8 [d- a- f] 1/8 [e- g c] 1/4 [b f d] [c e- a-] \
        [g d b] [a c e- f+] [f d b] [c e-] \
        1/2 [-f+ a] g _ _ 1/4 +e- d c b \
        1/8 [-c e- g c] . 1/16 . +g c e- g a- g f e- d c b- \
        a- g f e- d e- f e- d c b a- g f e- d \
        |100 1/16 [-c e- g c] 4/16 . 1/16 ++g c e- g a- g f e- d c b- \
        a- g f e- d e- f e- d c b a- g f e- d \
        *2 c d e- f g a b c d c b a g f e- d * \
        c d e- f g a b c b- a- g f e d c b- \
        a- b- c d e f g a- g f e d c b- a- g \
        1/8 [g- -g-] 3/8 . 10/4 . \
    ')
    # measures 117

    ns = NoteSet()
    #ns.append_ns([rh_1_49, lh_1_49])
    ns.append_ns([lh_50_117, rh_50_117])
    ns.set_tempo(120)
    ns.done()
    return ns

def main():
    ns = make_score()
    #ns.perf_dur_rel(1.3)
    #ns.print()
    ns.write_midi('data/app57.midi')
    pianoteq.play('data/app57.midi')

main()
