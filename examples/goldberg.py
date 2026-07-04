# aria from Bach's Goldberg variations
# it's mostly 3 voices (soprano/tenor/bass)
# Occasionally there's a 4th voice, alto.

import numula_path
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

soprano = sh_score(' \
    |1 1/4 g6 g 3/16 orn[(21)0 g a b 1/8 rep=2] 1/16 b \
    |2 1/8 a orn[2 - f+ g 1/16] 1/2 orn[2 - d e 1/8] \
    |3 1/4 orn[(21)0 f5+ g a 1/8 rep=2] 3/8 orn[210(12) f+ g a rep=2 1/4] 1/16 f+ g \
    |4 1/32 a g 1/16 f+ 1/32 g f+ 1/16 e 1/2 orn[2 - d e 1/8] \
    |5 1/4 d d 3/16 orn[(21)0 d e f 1/8 rep=2] 1/16 f \
    |6 1/8 e orn[2 - c d 1/16] 3/8 orn[2 - a b 1/8] 1/8 orn[2010 +e f+ g 1/8] \
    |7 <1/32 3/32> g + a g f+ e d c 3/16 orn[0 c +a 1/16] 1/16 -c \
    |8 1/32 b 3/32 g 1/8 f+ 1/2 orn[01(21)0 f+ g a 1/4] \
    |9 1/4 b b 3/16 orn[(21)0 b c+ d rep=2] 1/16 d \
    |10 d c+ b 9/16 a \
    |11 1/4 [g b e g] 3/8 orn[2101(21)0 f+ g a 1/4 rep=2] 1/16 f+  \
    |12 1/8 g orn[2 - e f+ 1/16] 3/8 orn[2101(21)0 b c+ d 1/4 rep=2] 1/8 e \
    |13 1/16 a g f+ e 1/8 d 9/32 a 1/32 b 1/16 c \
    |14 1/16 b a g f+ 1/8 e 9/32 orn[1 - +c+ d 1/8] 1/32 d 1/16 e \
    |15 1/16 d c+ b a 1/8 +g 1/4 -b 1/8 c+ \
    |16 5/32 orn[0 c+ d 1/8] 1/32 e d c+ 1/2 orn[0 c+ d 1/8] \
    |17 \
').tag('soprano')

alto = sh_score(' \
    |1 1/4 . . d5 . . d . . c+ . . a \
    |5 . . g . . a 3/4 . . \
    |9 1/4 . . +e 3/4 . . . \
    |13 1/4 . . 3/4 . . 3/8 . 1/8 a 1/4 d \
    |17 \
').tag('alto')

tenor = sh_score(' \
    |1 <1/4 1/2> . b4 . a . g . f+ \
    |5 . d 1/4 . 3/8 e 1/8 . \
    |7 1/8 . 3/8 c5 1/16 b a g f+ e f+ 1/8 g a 1/2 b \
    |9 1/4 . 1/2 b 1/4 a . . \
    |11 1/8b 3/8 e 1/8 d c+ d 1/2 e \
    |13 1/4 . 1/2 a4 1/4 b e f+ 3/16 e 1/16 f+ 1/2 g f+ \
    |17 \
').tag('tenor')

bass = sh_score(' \
    |1 3/4 g4 f+ e 5/8 d 1/8 c \
    |5 3/4 b 5/8 c 1/8 d \
    |7 e c 1/2 d 3/8 -g 1/8 +d 3/16 orn[(21)0 d e f+ 1/8] 1/16 f+ \
    |9 4/4 g 1/8 orn[21 - f+ g 1/16 rep=2] e f+ b \
    |11 3/8 -e 1/8 e f+ g 3/8 a 1/8 b a g \
    |13 3/4 f+ g a -d \
    |17 \
').tag('bass')

def main():
    ns = Score(tempo=60)
    ns.append_scores([
        soprano,
        alto,
        tenor,
        bass
    ])
    print(ns)
    numula.pianoteq.play_score(ns)

main()
