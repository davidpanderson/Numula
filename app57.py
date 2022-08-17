# Beethoven sonata op 57, 3rd mvt

from note import *
from notate import *
from nuance import *
import pianoteq

def make_score():
    rh1 = n('1/16 \
        . *2 \
        *2 -c f a- c d- c b- | a- b- a- g f g a- f . * \
        d- g- b- d- e- d- c | b- c b- a- g- a- g- f \
        e f g e f g a- f | g a- b- g e f g e f * \
    ')
    lh1 = n('*2 #f2 1/4 f . . 3/16 . 1/16 +f * \
        1/4 -b- . . 3/16 . 1/16 d- \
        1/8 c . d- . b- . c . \
        *2 #f2 1/4 [f +f] 3/16 . 1/16 #c6 [c -a-] 1/4 [c -a-] [a- f] * \
        #c3 1/4 [b- +b-] 3/16 . 1/16 #c6 [b- d-] 1/2 [b- d-] \
        1/8 [c b-] [--c -c] . [d- +d-] . [b- -b-] . [c +c] \
    ')

    ns = NoteSet()
    ns.append_ns([rh1, lh1])
    ns.done()
    return ns

def main():
    ns = make_score()
    ns.print()
    ns.write_midi('data/app57.midi')
    pianoteq.play('data/app57.midi')

main()
