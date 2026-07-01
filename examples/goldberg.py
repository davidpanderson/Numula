# aria from Bach's Goldberg variations
# it's mostly 3 voices (soprano/tenor/bass)
# Occasionally there's a 4th voice, alto.

import numula_path
from numula.nuance import *
import numula.pianoteq

soprano = sh_score(' \
    |1 1/4 g6 g 3/16 a 1/16 b 1/8 a f+ 1/2 d \
    |3 1/4 g5 3/8 g 1/16 f+ g 1/32 a g /16 f+ 1/32 g f+ 1/16 e 1/2 d \
    |5 \
').tag('soprano')

alto = sh_score(' \
    |1 1/4 . . d5 . . d . . c+ . . a \
    |5 \
').tag('alto')

tenor = sh_score(' \
    |1 1/4 . 1/2 b4 1/4 . 1/2 a 1/4 . 1/2 g 1/4 . 1/2 f+ \
    |5 \
').tag('tenor')

bass = sh_score(' \
    |1 3/4 g4 f+ e 5/8 d 1/8 c \
    |5 \
').tag('bass')

def main():
    ns = Score(tempo=60)
    ns.append_scores([
        soprano,
        alto,
        tenor,
        bass
    ])
    numula.pianoteq.play_score(ns)

main()
