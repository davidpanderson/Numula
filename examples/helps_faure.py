# Robert Helps: Hommage a Faure

from numula.nscore import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

r1 = '<1/2 1/4 1/4 3/4 1/4 1/4 1/4 1/4 1/4 4/4>'
r2 = '<1/2 1/4 1/4 2/4 1/4 1/4 1/4 1/4 1/4 1/4 4/4>'

soprano = n(f'meas4/4 \
    |1 {r1} b-6 a- b- c- b- b- a- g- a- b- \
    |5 {r2} g- f g- b- a- g- g- f e- f g- \
    |9 {r1} b-6 a- b- c- b- b- a- g- a- b- \
    |13 g- f g- b- a- g- f c d e- \
    |17 +b- a- b- c- b- b- a- g- a- b- \
    |21 {r2} g- f- g- b- a- g- g- f e- f g- \
    |25 {r1} b- a- b- c- b- b- a- g- a- b- \
    |29 {r2} g- f g- b- a- g- g- f c d \
    |32 meas2/4 1/2 e- \
    |33 meas4/4 {r1} +b- a- b- c- b- b- a- g- a- b- \
    |37 \
')

alto = n('meas4/4 \
    |1 1/4 . [a-5 d-] . [d- e-] . [c- d-] . d- \
    |3 . [c- d-] . [c- d-] . [a- d-] . [e- f] \
    |5 . [-a- g-] . +d- . [d- c-] . d- \
    |7 . -g- . b- . [d- -g-] . . \
    |9 . [a- d-] . d . [d- c-] . c- \
    |11 . [c- d-] . c- . [d- a-] . [b- +f] \
    |13 . [-a- g-] . a- . [a- d-] . d- \
    |15 . c . c 4/4 . \
    |17 \
')

bass = n('meas4/4 \
    |1 1/8 f5 -b- d- -e- ++a- 1/4 d- 1/8 _ e- -e- \
    |2 -a- +g- +d- c- +g- d- e- -g- \
    |3 +g- -c- e- --d- ++g- 1/4 -c- 1/8 _ d- -d- \
    |4 ++a- -b- d- -e- ++a- 1/4 e- 1/8 _ g d- \
    |5 b- -c- ++d- a- +f -b- e- -g- \
    |6 g- -a- ++d- -g- ++a- -c- e- a- \
    |7 c- --b- +a- c- +g- -c- e- 1/4 a- 1/8 e- +b- d- f e- +b- -e- \
    |9 a- -d- b- +b- a- -d- d -e \
    |10 e -a- +e- +d- g- -c- d- -g- \
    |11 +g- -c- e- --d- ++g- 1/4 -c- 1/8 _ d --d- \
    |12 +b- -e- ++f d- +a- 1/4 -d- 1/8 _ e- -g \
    |13 b- a- d- --c- ++f -b- e- -g- \
    |14 e- -a- +g- +d- +c- -e- g- -b- \
    |15 a- -b- ++c d +b- -c +g -a- \
    |16 a- -b- +g- b- +f e- d- a- \
    |17 \
')

def main():
    ns = Score(tempo=80)
    ns.append_score([
        soprano,
        alto,
        bass
    ])
    print(ns)

main()
