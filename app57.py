# Beethoven sonata op 57, 3rd mvt

from nscore import *
from notate_score import *
from nuance import *
from notate_nuance import *
from vol_name import *
import pianoteq

rh_20_117 = n(' \
    |20 1/16 . *2 \
    *2 -c f a- c d- c b- | a- b- a- g f g a- f . * \
    d- g- b- d- e- d- c | b- c b- a- g- a- g- f \
    e f g e f g a- f | g a- b- g e f g e f * \
    |36 *2 c5 f a- c -c f a- . * \
    -b d +a- b -b d +a- b -b e g c -c e g \
    *3 . -c e g c -c e g * c -c e g c -c f a- \
    *3 . -f a c f -f a c * \
    [-f a] +f [-f b-] +f [-f +c] f [-f +d-] f \
    . --c f a- c -c f a- c -c +g b- c -c e g \
    |50 1/4 [c5 f a- c] 3/16 . 1/16 [f a-] 1/4 [f a-] 3/16 . 1/16 [f a-] \
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
').tag('rh')

lh_20_117 = n(' \
    *2 1/4 f2 . . 3/16 . 1/16 +f * \
    1/4 -b- . . 3/16 . 1/16 d- \
    1/8 c . d- . b- . c . \
    *2 1/4 [f2 +f] 3/16 . 1/16 #c6 [c -a-] 1/4 [c -a-] [a- f] * \
    #c3 1/4 [b- +b-] 3/16 . 1/16 #c6 [b- d-] 1/2 [b- d-] \
    1/8 [c b-] [--c -c] . [d- +d-] . [b- -b-] . [c +c] \
    |36 1/4 [--f +f] 3/16 . 1/16 [+f a-] 1/4 [a- f] 3/16 . 1/16 [a- f] \
    1/2 [a- f c] 1/8 [c e g] . 1/4 . [-c -c] 3/16 . 1/16 [++g b-] \
    1/4 [g b-] 3/16 . 1/16 [g b-] 1/2 [f g b-] \
    1/8 [f a-] . 1/4 . [f -f] 3/16 . 1/16 [++c e-] 1/4 [c e-] 3/16 . 1/16 [c e-] \
    |46 5/8 [b- c e-] 1/8 [d- b-] [c a-] [b- g] \
    1/4 [a- f c] 3/16 . 1/16 [f a-] 1/4 [b- g -c] 3/16 . 1/16 [e g] \
    1/16 -f +c a- f c +a- f c a- +f c a- f +c a- f \
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
    1/2 f+ 1/4 _ a 1/2 [g -g] 1/4 _ _ +e- d \
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
').tag('lh')

rh_118_211 = n(' \
    |118 1/16 *2 . a c e- g- a- g- f e- f e- d- c d- e- c * \
    . a c e- g- a- g- f *2 1/8 e- 1/16 e- f g- a- g- f * \
    |125 1/8 e- par+12 g- f a 1/16 b- par \
    *2 f b- d- f g- f e- d- e- d- c b- c d- b- . * \
    g- c- e- g- a- g- f e- f e- d- c- d- e- c- b- c b- a b- c d- b- \
    |133 a b- a g a b- c a 1/8 b- 1/16 b- d- f g- f e- \
    |135 d- e- d- c b- c d- b- \
    |136 . . b- d- f g- f e- 1/4 _ _ _ b6- a b- \
    |137 1/16 -d- e- d- c b- c d- b- 1/4 _ b6- \
    1/16 [c6- +c-] -g- c- e- g- a- g- f \
    |139 e- f e- d- c- d- c- b- a c e- d- c d- c b- a b- a g- f e- d- c \
    |142 1/8 b- 1/4 +f 1/8 f f 1/4 g- 1/8 g- g- 1/4 f 1/8 f f c d- e- \
    d- par+12 1/4 f 1/8 f f 1/4 g- 1/8 g- g- 1/4 f 1/8 f f c d- e- \
    |150 d- par 1/4 c 1/8 c c 1/4 b 1/8 b b 1/4 c 1/8 c c g a- b- a- \
    par+12 1/4 c 1/8 c c 1/4 b 1/8 b b 1/4 c 1/8 c c g a- b- 1/16 a- par \
    -c f a- c d- c b- a- b- a- g f g a- f g- d- g- b- d- e- d- c \
    |161 b- c b- a- g- a- b- g- a -e- a c e- f e- d- \
    |163 c d- c b- a b- c a \
    |164 b- f b- d- f g- f e- d- c b- a- g- f e- d- \
    c b- a- g- f e- d- c b- c d- c 1/8 b- [b d f a- ] \
    |168 1/16 [g e c] par+12 c *7 . c * \
    #c5 *8 . c * #c6 *8 . c * #c7 *8 . c * par \
    |176 1/16 . d4- g- b- d- --b- d- g- \
    |177 b- d- g- b- d- --b- d- g- b- d- g- b- 1/8 d- . 1/2 . \
    |180 1/16 . e4 g b- +e --c +g b- c e g b- +e --c +g b- \
    |182 c e g b- 1/8 +e . 46/4 . \
    |206 1/2 [g3 b- c e] . *3 [g b- c e] * [g3 b- c e] \
    |212 \
', 1/2).tag('rh')

lh_118_211 = n(' \
    |118 1/4 ---f . . 3/16 . 1/16 +f 1/4 -f . . 3/16 . 1/16 +f \
    |122 1/4 -f 1/16 . . +++a b- *2 c d- c b- 1/8 a 1/16 a b- * \
    c d- c b- a g- f e- *2 2/2 d- _ 1/16 . f *7 b- f * * \
    |130 2/2 e- _ 1/16 . g- *7 c- g- * \
    1/2 f _ 1/16 . b- *3 d- b- * 1/2 -e- _ 1/16 . f *3 +c -f * \
    |134 *2 -d- ++f . .  1/4 -b- a b- _ _ _ 1/16 *3 . d- f d- * * \
    |138 -e- [++g- c-] *7 -e- [g- c-] * *4 -f [a c e-] * \
    -f a f a --f +f -f +f \
    |142 1/8 --b- 1/16 *4 [b4- d-] f * *3 [-b- d-] e * \
    [-a c] e *7 [-a c] f * *5 [-b- d-] f * *3 [-b- d-] e * \
    |148 [-a c] e *7 [-a c] f * \
    [-b- d-] f *3 [e4 g] c * [-f a-] c *3 [-f a-] +d * \
    |152 [-e g] +d *7 [-e g] c * *5 [-f a-] c * *3 [-f a-] +d * \
    |156 [-e g] +d *7 [-e g] c * \
    |158 1/4 [--f a- c f] 1/16 . c f a- c d- c b- a- b- c a- \
    |160 b- c b- a- g- d- g- b- \
    |161 d- e- d- c b- c d- b- \
    c d- c b- a -e- +a c \
    |163 e- f e- d- c d- e- c \
    d- -f b- d- f g- f e- d- c b- a- g- f e- d- \
    c b- a- g- f e- d- c b- c d- c 1/8 b- b \
    |168 c e c f c +g -c +a- -c +b- -c +a- -c +g -c f \
    c e c f c +g -c +a- -c +a -c +b- -c +b -c +c \
    |176 [b- g- d- b- ] 15/8 . 1/8 [c +g b- c] 15/8 . \
    |184 1/12 d3- +d- e 1/16 g b- d- e 1/8 g . . . \
    1/12 e3 +e g 1/16 b- d- e g 1/8 b- . . . \
    1/12 g3 +g b- 1/16 d- e g b- 1/8 d- . . . \
    1/12 b3- +b- d- 1/16 e g b- d- 1/8 e . . . \
    |192 d4- e g b- d- e g b- d- e g b- d- e g b- \
    g e d- b- g e d- b- g e d- b- g e d- b- \
    1/2 g e d- b- 2/2 g 47/16 c 1/16 c \
    |212 \
', 1/2).tag('lh')

rh_212_299 = n(' \
    |212 1/16 *2 . c4 f a- c d- c b- a- b- a- g f g a- f * \
    . d- g- b- d- e- d- c b- c b- a- g- a- g- f \
    |218 e f g e f g a- f g a- b- g e f g e \
    |220 1/4 f 1/8 . +e f g a- f . . . par+12 e f g a- f \
    . . . f g- b- d- d- 1/4 d- 1/2 c 1/4 -e 1/16 \
    |228 f par *2 c5 f a- c -c f a- . * \
    -b d +a- b -b d +a- b -b e g c -c e g \
    *3 . -c e g c -c e g * c -c e g c -c f a- \
    |236 *3 . -f a c f -f a c * \
    [-f a] +f [-f b-] +f [-f +c] f [-f +d-] f \
    . --c f a- c -c f a- c -c +g b- c -c e g \
    1/4 [c5 f a- c] 3/16 . 1/16 [f a-] 1/4 [f a-] 3/16 . 1/16 [f a-] \
    |244 1/2 [f a-] 1/8 [g e] 5/8 . 3/16 . 1/16 [g b-] 1/4 [g b-] \
    3/16 . 1/16 [g b-] 1/2 [g b-] 1/8 [a- f] 5/8 . 3/16 . 1/16 [+c e-] \
    1/4 [c e-] 3/16 . 1/16 [c e-] 5/8 [c e-] \
    1/8 [d- b-] [c a-] [b- g] 1/4 [f a-] \
    3/16 . 1/16 [f a- +f] 1/4 [g -b- g] 3/16 . 1/16 [e g +e] [f -a- f] \
    *2 c f a- c d- c b- a- b- a- g f g a- f . * \
    g- +c e- g- a- g- f e- f e- d- c d- e- c \
    . -g- +c e- g- a- g- f e- f e- d- c b- a- g- \
    |264 f *2 a- d- f a- b- a- g- f g- f e- d- e- f d- . * \
    *2 g- a- g- a- g- f g- . e f e . f g f . * \
    g- a- g- a- g- f g . e f e . d- e- d- . c d- c . b c b \
    |275 . b- c b- . a- b- a- . a- b- a- . g a- g . f g f . e f e \
    |278 #c5 *2 . +d- *3 +d- -d- * . d- +d- c b- a- g f * \
    . d5- *3 +d- -d- * . +d- -d- +d- . +d- -d- +d- \
    |284 . c -c +c . b -b +b . b- -b- +b- . a- [-c a-] +a- \
    . a- [-d -a-] +a- . g [d -g] +g . f [-a- f] +f . e [-g e] +e \
    |288 [f -a- f] c f a- c d- c b- a- b- a- g f e- d- c \
    b- a- g f 1/8 e [c e g c] *4 [-c e +b- c] * \
    1/16 [-c f a- c] +c f a- c d- c b- a- b- a- g f e- d- c \
    |294 b- a- g f 1/8 e [c e g c] *4 [-c e +b- c] * \
    1/4 [-c f a- c] 1/8 . [c f a- c] *4 [-c e +b- c] * \
    1/4 [-c f a- c] 1/8 . [-c a- f c] *4 [+c b- -e c] * \
    |300 \
', 1/2).tag('rh')

lh_212_299 = n(' \
    |212 1/4 [f3 -f] . . . [f +f] 3/16 . 1/16 [c6 a-] 1/4 [c a-] 1/8 [a- f] . \
    1/4 [b3- -b-] 3/16 . 1/16 [b5- d-] 1/2 [b- d-] \
    |218 1/8 [b- c] par-12 c4 . d- . b- . c 1/16 -f par \
    +c f a- c d- c b- a- b- a- g f g a- f \
    a- -c f a- c d- c b- a- b- a- g f g a- f \
    |224 b- -d- g- b- d- e- d- c b- c b- a- g- a- g- f \
    e f g a- b- a- g f e f e d- c b- a- g \
    |228 1/4 f3 3/16 . 1/16 [+f a-] 1/4 [f a-] 3/16 . 1/16 [f a-] \
    |230 1/2 [-c f a-] 1/8 [g e c] . 1/4 . \
    1/4 [c -c] 3/16 . 1/16 [g4 b-] 1/4 [g b-] 3/16 . 1/16 [g b-] \
    |234 1/2 [b- g f] 1/8 [f a-] . 1/4 . [f -f] 3/16 . 1/16 [c5 e-] \
    1/4 [c e-] 3/16 . 1/16 [c e-] 5/8 [e- c b-] 1/8 [d- b-] [c a-] [b- g] \
    |240 1/4 [a- f c] 3/16 . 1/16 [f a-] 1/4 [-c +g b-] 3/16 . 1/16 [g e] \
    |242 f +c a- f c +a- f c a- +f c a- f +c a- f \
    c f a- c b c b c b c g c -e +c g c \
    |246 -c e g c -e g c e -g c e g -c e g c \
    -f a- c f e f e f e f c f -a- +f c f \
    |250 -f a c f -a c f a -c f a c -f a c f \
    -a +f e f -a +f -a +f -a +f -b- +f c f d- f \
    |254 c5 f a- c b c b c -c e g c -c +g b- c \
    |256 *2 f4 [+f a-] *7 [+c -c] [f a-] * * \
    |260 *2 a3- [+g- a-] *7 [c -e-] [g- a-] * * \
    |264 d4- [+d- f] *7 [a- -a-] [d- f] * \
    |266 d4- [+d- f] [a- -a-] [d- f] 1/8 a- d- f a- d- d- \
    |268 *2 3/8 [d- b-] 1/8 [a- c] 1/4 [b- g] [a- c] * \
    |272 3/8 [b- d-] 1/8 [c a-] 1/4 [b- g] [f a-] [g e] [f d] [f d-] [f c] \
    |276 1/2 b5 [c -c] _ _ 1/4 . d6 -a- g \
    |278 *2 3/8 [g4- d- b-] 1/8 [a- c f] 1/4 [e -b- g] [a- c f] * \
    |282 3/8 [g4- d- b-] 1/8 [a- c f] 1/4 [e -b- g] [f a- d-] \
    |284 [c g e] [d f a- b] [b- g e] [f a-] \
    1/2 b2 c _ _ 1/4 a3- g f e \
    |288 1/8 [f c a- f] . 1/16 . c4 f a- c d- c b- a- g f e- \
    d- c b- a- g a- b- a- g f e d c b- a- g \
    |292 1/8 [f a- c f] . 1/16 . c5 f a- c d- c b- a- g f e- \
    d- c b- a- g a- b- a- g f e d c b- a- g \
    |296 *2 f g a- b- c d e f g f e d c b- a- g * \
    |300 \
', 1/2).tag('lh')

# first ending 300-307
rh_300_307 = n(' \
    |300 1/8[c f a- c] *3 [+c a- f c] * *4 [+c b- -e c] * \
    1/16 [c e- +a c] a4 d e- g- a c e- g- a c e- g- e- c a \
    g- e- c a g- e- c a g- e- c a g- e- c a *4 g- +e- c a * \
    |308 \
', 1/2).tag('rh')
lh_300_307 = n(' \
    |300 \
    1/16 f3 e d c b- a- g f g a- b- c d e f g 1/8 [g- -g-] . . . 10/4 . \
    |308 \
', 1/2).tag('lh')

# second ending onward
rh_300_end = n(' \
    |300 1/16 [c f a- c] g a- b- c d e f \
    *2 g f e d- c b- a- g f g a- b- c d e f * \
    *8 g f+ * g f e d- c b- a- g \
    |presto \
    1/2 [f c a-] [a- c +a-] \
    1/8 (stac *2 [g -b- g] [g b- +e] [c b- g] [g b- +e] \
    [f c a-] [a- c] [f c a-] [a- c +a-] * \
    [g -c g] [g c e-] [d b g] [g b +g] stac) \
    |315 1/4 -c 1/8 . 1/24 c d e \
    1/2 [f c a-] [a- c +a-] \
    1/8 (stac *2 [g -b- g] [g b- +e] [c b- g] [g b- +e] \
    [f c a-] [a- c] [f c a-] [a- c +a-] * \
    [g -c g] [g c e-] [d b g] [g b +g] stac) \
    |316 1/4 -c 1/8 . 1/24 e- f g \
    |317 \
    1/2 [a- e- c] [c e- +c] \
    1/8 (stac *2 [b- -d- b-] [b- d- g] [e- d- b-] [b- d- g] \
    [a- e- c] [c e-] [a- e- c] [c e- +c] * \
    [a e- c] [c e- f] [a e- c] [c e- +c] \
    [b- f d-] [d- f] [b- f d-] [d- f +d-] \
    [c -f c] [c f a-] [g e c] [c e +c] stac) \
    |325 1/4 -f 1/8 . 1/24 e- f g \
    1/2 [a- e- c] [c e- +c] \
    1/8 (stac *2 [b- -d- b-] [b- d- g] [e- d- b-] [b- d- g] \
    [a- e- c] [c e-] [a- e- c] [c e- +c] * \
    [a e- c] [c e- f] [a e- c] [c e- +c] \
    [b- f d-] [d- f] [b- f d-] [d- f +d-] \
    [c -f c] [c f a-] [g e c] [c e +c] stac) \
    |326 \
    1/16 #c5 f c f a- c d- c b- a- b- a- g f g a- f a- -c f a- c d- c b- \
    |328 a- b- a- g f g a- f g- d- g- b- d- e- d- c \
    |330 b- c b- a- g- a- g- f e f g a- b- a- g f e f g a- b- c d e \
    |333 f c f a- c d- c b- a- b- a- g f g a- f \
    a- -c f a- c d- c b- a- b- a- g f g a- f \
    g- d- g- b- d- e- d- c b- c b- a- g- a- g- f \
    |339 e f g a- b- a- g f e f g a- b- c d e \
    |341 *4 f -a- c f 5/16 a- 1/16 -c f a- c a- g e * \
    |349 *3 f c f a- c a- g e * *2 +c a- g e * \
    +c a- f c +a- f c a- +f c a- f +c a- f c \
    +a- f c a- +f c a- f +c a- f c +a- f c a- \
    +f c a- f +c a- f c +a- f c a- +f c a- c \
    1/8 [a- c f] . . . [+f a- c f] . . . [-f c a- f] . . . \
    |362 \
').tag('rh')
lh_300_end = n(' \
    |300 1/4 f3 1/8 . [c f a- c] *4 [-c e g b- c] * \
    |302 1/4 [-c f a- c] 1/8 . [c f a- c] *4 [-c e g b- c] * \
    |304 1/4 [c a- f c] 1/8 . [c a- f c] *12 [+c b- g e c] * \
    |308 1/2 *2 [f2 a- c f] * \
    1/8 (stac *2 [+c -c] c c c [-f +f] f f f * -g +g -g g stac) \
    1/4 c 1/8 . 1/32 c b- a- g \
    |316 1/2 *2 [f2 a- c f] * \
    1/8 (stac *2 [+c -c] c c c [-f +f] f f f * -g +g -g g stac) \
    1/4 c 1/8 . 1/24 e- f g \
    |324 1/2 *2 [+a- e- c a-] * 1/8 (stac *2 [e3- +e-] -e- e- e- [a- -a-] +a- a- a- * \
    |330 [f -f] f f f [b- +b-] b- b- b- -c +c -c c stac) \
    1/4 [f -f] 1/8 . 1/24 +e- f g \
    1/2 *2 [+a- e- c a-] * 1/8 (stac *2 [e3- +e-] -e- e- e- [a- -a-] +a- a- a- * \
    |340 [f -f] f f f [b- +b-] b- b- b- -c +c -c c stac) \
    |343 1/16 [-f +f] *3 +p #c3 1/16 f a- c 5/16 f -p * \
    1/16 +p -f a- c 1/4 f -p 1/16 . +p -b- d- g- 5/16 b- -p \
    1/16 +p -b- d- g- 1/4 b- -p \
    1/16 . +p -c +g b- 5/16 c -p 1/16 +p -c +g b- 1/4 c -p \
    |351 1/16 . *3 1/16 +p -f a- c 5/16 f -p * 1/16 +p -f a- c 1/4 f -p \
    1/16 +p . -b- d- g- 5/16 b- -p 1/16 +p -b- d- g- 1/4 b- -p \
    |357 1/16 . +p -c e g 1/4 c -p 1/16 . +p --c e g 1/4 c -p \
    |359 1/8 [-f -f] \
    *3 1/8 . . 1/16 +p c6 f 3/8 a- -p 1/8 --c f * \
    . . 1/16 +p +c f 3/8 a- -p \
    1/8 --c 1/4 f 1/8 . c 1/4 -f 1/8 . c 1/4 -f 1/8 . c -f +c -f +c \
    |371 1/16 *12 -f a- c f * 1/8 *3 [-f a- c f] . . . * \
    |380 \
').tag('lh')

# volume:
# for each hand, we generate two PFTs:
# one for continuous change,
# the other for single-note and short-scale adjustment

# measures 20..107 are analogous to 212..219

def v20_117(ns, t0):
    rhv = vol(' \
        |20 *2 *3 ppp 3/4 p 1/4 ppp * 1/2 p 1/2 ppp * \
        |36 *2 [ pp 4/2 p * \
        |44 [ pp 6/4 p 1/2 pp 2/2 pp \
        |50 \
    ', 1/2)
    rha = accents(' \
        |20 *2 \
            *3 mm 1/4 f 1/4 mf_ 1/4 mf 1/4 * \
            1/8 f 1/4 f 1/4 f 1/4 f 1/8 \
        * \
        |36 *2 *3 mm 1/4 f 1/4 * f 1/4 f 1/4 * \
        |44 *3 mm 1/4 _f 1/4 * mm 1/2 *4 _f 1/4 * \
        |50 \
    ', 1/2)
    ns.vol_adjust_pft(rhv, t0, lambda n: 'rh' in n.tags)
    ns.vol_adjust_pft(rha, t0, lambda n: 'rh' in n.tags)
        
    lhv = vol(' \
        |20 *2 p 4/2 mp 4/2 p * \
        |36 *3 p 2/2 mp 2/2 p * p 1/2 mp 1/2 p \
        |50 \
    ', 1/2)
    lha = accents(' \
        |20 *3 mf 2/2 * mf 1/2 mf 1/2 \
        |28 *3 1/2 mf 1/2 * 2/2 \
        |36 *3 2/2 mf 2/2 * *2 mp 1/2 * \
        |50 \
    ', 1/2)
    ns.vol_adjust_pft(lhv, t0, lambda n: 'lh' in n.tags)
    ns.vol_adjust_pft(lha, t0, lambda n: 'lh' in n.tags)

    lhv = vol(' \
        |50 *2 p 2/2 mp 1/2 mp 1/2 p * \
        |58 [ mp 2/2 mf 2/2 mp 2/2 mf \
        |64 ] *5 mp 1/2 mf 1/2 mp * \
        |74 mp 2/2 mf \
        |76 *2 *2 [ mf 1/2 mp 1/2 mf * [ mp 4/2 f 2/2 mp * \
        |96 *2 [ mf 4/2 f * ] \
        |104 *4 mf 1/2 f 1/2 mf * \
        |112 [ ff 6/2 ff \
        |118 \
    ', 1/2)
    ns.vol_adjust_pft(lhv, t0+30/2, lambda n: 'lh' in n.tags)

def t20_117(ns, t0):
    x = tempo(' \
        |20 *2 *4 60 1/2 65 1/2 55 .1p * * \
        |36 *2 60 2/2 65 2/2 60 * \
        60 2/2 65 50 2/2 60 2/2 60 \
        |50 \
    ', 1/2)
    ns.tempo_adjust_pft(x, t0)

def p20_117(ns, t0):
    # virtual pedal RH arpeggios starting in m16
    rh = pedal(' \
        |20 - 16/2 *2 *3 + 1/2 * + 1/4 + 1/4 * \
        |44 *3 + 1/2 * *4 + 1/8 * *2 + 1/2 * \
        |50 \
    ', 1/2)
    ns.vsustain_pft(rh, t0, lambda n: 'rh' in n.tags)
    ns.insert_pedal(PedalUse(t0+92/2, 6/2))

    lh = pedal(' \
        |50 *2 + 1/4 1/4 1/4 1/4 1/4 - 3/4 * \
        |58 + 1/4 1/4 1/4 1/4 - 2/2 + 1/4 - 1/4 + 1/2 \
        |64 + 2/2 2/2 *2 + 1/2 1/4 1/4 * \
        |72 *2 + 2/2 * \
        |76 - 42/2 \
        |118 \
    ', 1/2)
    ns.vsustain_pft(lh, t0+30/2, lambda n: 'lh' in n.tags)

def v118_211(ns, t0):
    rh = vol(' \
        |118 *2 pp 1/2 _p 1/2 pp * pp 3/2 mp 1/2 pp \
        |126 *2 pp 1/2 _p 1/2 pp * pp 2/2 mp 2/2 mp \
        |134 [ pp 4/2 f 4/2 pp \
        |142 [ p 4/2 p ] f 4/2 f ] p 4/2 p ] f 4/2 f \
        |158 f 6/2 ff 4/2 f \
        |168 [ mf 2/2 f 2/2 mf 4/2 ff 8/2 ff \
        |184 [ p 8/2 pp 20/2 pp \
        |212 \
    ', 1/2)
    rha = accents(' \
        |118 24/2 \
        |142 *2 *3 1/8 mf 3/8 * 1/2 *3 1/8 f 3/8 * 1/2 * \
        |158 54/2 \
    ', 1/2)
    lh = vol(' \
        |118 p 7/2 p 1/2 pp \
        |126 pp 4/2 pp [ p 2/2 p [ _p 2/2 _p \
        |134 *2 [ pp 1/2 mp 1/2 pp * [ f 4/2 pp \
        |142 pp 4/2 pp [ mp 4/2 mp ] pp 4/2 pp [ mp 4/2 mp \
        |158 [ mf 6/2 f 4/2 p \
        |168 [ p 2/2 mp 2/2 p 4/2 f \
        |176 [ ff 8/2 ff [ p 8/2 pp 20/2 pp \
        |212 \
    ', 1/2)
    ns.vol_adjust_pft(lh, t0, lambda n: 'lh' in n.tags)
    ns.vol_adjust_pft(rh, t0, lambda n: 'rh' in n.tags)
    ns.vol_adjust_pft(rha, t0, lambda n: 'rh' in n.tags)
    
def t118_211(ns, t0):
    t = tempo(' \
        |118 *2 p0.1 60 2/2 60 * p0.1 4/2 55 \
        |126 55 8/2 60 8/2 55 \
        |142 34/2 65 \
        |176 8/2 65 55 28/2 50 \
        |212 \
    ', 1/2)
    ns.tempo_adjust_pft(t, t0)

def p118_211(ns, t0):
    lh = pedal(' \
        |118 8/2 *3 + 2/2 * 1/2 1/2 \
        |134 *2 - 1/4 + 1/4 1/4 1/4 * \
        |138 2/2 1/2 1/4 1/4 \
        |142 *2 *2 5/8 3/8 1/8 7/8 * * \
        |158 - 54/2 \
        |212 \
    ', 1/2)
    p = pedal(' \
        |118 - 58/2 \
        |176 *2 + 7/4 - 1/4 * \
        |184 *4 + 3/4 - 1/4 * \
        |192 + 13/2 - 1/2 + 6/2 \
        |212 \
    ', 1/2)
    ns.vsustain_pft(lh, t0, lambda n: 'lh' in n.tags)
    ns.pedal_pft(p, t0)

def v212_299(ns, t0):
    rhv = vol(' \
        |212 *2 *3 ppp 3/4 p 1/4 ppp * 1/2 p 1/2 ppp * \
        |228 *2 [ pp 4/2 p * \
        |236 [ pp 6/4 p 1/2 pp 2/2 pp \
        |242 \
    ', 1/2)
    rha = accents(' \
        |212 *2 \
            *3 mm 1/4 f 1/4 mf_ 1/4 mf 1/4 * \
            1/8 f 1/4 f 1/4 f 1/4 f 1/8 \
        * \
        |228 *2 *3 mm 1/4 f 1/4 * f 1/4 f 1/4 * \
        |236 *3 mm 1/4 _f 1/4 * mm 1/2 *4 _f 1/4 * \
        |242 \
    ', 1/2)
    ns.vol_adjust_pft(rhv, t0, lambda n: 'rh' in n.tags)
    ns.vol_adjust_pft(rha, t0, lambda n: 'rh' in n.tags)
        
    lhv = vol(' \
        |212 *2 p 4/2 mp 4/2 p * \
        |228 *3 p 2/2 mp 2/2 p * p 1/2 mp 1/2 p \
        |242 \
    ', 1/2)
    lha = accents(' \
        |212 *3 mf 2/2 * mf 1/2 mf 1/2 \
        |220 *3 1/2 mf 1/2 * 2/2 \
        |228 *3 2/2 mf 2/2 * *2 mp 1/2 * \
        |242 \
    ', 1/2)
    ns.vol_adjust_pft(lhv, t0, lambda n: 'lh' in n.tags)
    ns.vol_adjust_pft(lha, t0, lambda n: 'lh' in n.tags)

def t212_299(ns, t0):
    pass
def p212_299(ns, t0):
    pass

def v300_end(ns, t0):
    v = vol(' \
        |300 f 8/2 _ff \
        |308 *2 [ ff 1/2 fff 1/2 fff [ p 5/2 mf ] mf 1/2 ff * \
        |324 ff 1/2 fff 1/2 fff [ mp 7/2 mf [ f 1/2 ff \
        |334 ff 1/2 fff 1/2 fff [ p 7/2 f \
        |343 [ f 8/2 f_ 8/2 _ff 8/2 ff_ \
        |367 [ _ff 4/2 ff 6/2 fff [ fff_ 3/2 fff_ \
        |380 \
    ', 1/2)
    ns.vol_adjust_pft(v, t0)
    a8 = 'mf'    # accents on 8th-note chords in 310 onward
    lha = accents(' \
        |300 *3 3/8 mf 5/8 * mf 1/2 mf 1/2 \
        |308 *2 2/2 *6 <a8> 1/2 * * \
        |324 2/2 *8 <a8> 1/2 * 2/2 *7 <a8> 1/2 * \
        |343 *16 1/4 mf 1/4 * \
        |359 *4 1/2 mf 1/2 * \
        |367 *10 mf 1/4 mf 1/4 * 3/2 \
        |380 \
    ', 1/2, locals())
    ns.vol_adjust_pft(lha, t0, lambda n: 'lh' in n.tags)
    rha = accents(' \
        |300 8/2 \
        |308 *2 2/2 *6 <a8> 1/2 * * \
        |324 2/2 *8 <a8> 1/2 * 2/2 *7 <a8> 1/2 * \
        |343 16/2 \
        |359 *4 1/4 mf 3/4 * \
        |367 2/2 1/4 mf 1/4 *7 mf 1/4 mf 1/4 * 3/2 \
        |380 \
    ', 1/2, locals())
    ns.vol_adjust_pft(rha, t0, lambda n: 'rh' in n.tags)
    ns.vol_adjust(
        .9,
        lambda n: 'ch' in n.tags and n.chord_pos < n.nchord-1
    )
    
def t300_end(ns, t0):
    t = tempo(' \
        |300 *3 60 2/2 p.05 * 60 2/2 70 \
        |308 *2 p.15 65 2/2 65 p.1 70 6/2 70 * \
        |324 p.15 70 10/2 70 \
        |334 p.15 70 9/2 70 \
        |343 70 34/2 70 \
        |377 50 3/2 50 \
        |380 \
    ', 1/2)
    ns.tempo_adjust_pft(t, t0)
    ns.pause_before(t0+8/2, .1, False)
    ns.pause_before(t0+10/2, .2, False)
    ns.pause_before(t0+18/2, .2, False)
    
def p300_end(ns, t0):
    p = pedal(' \
        |300 - 8/2 *2 - 3/4 - 1/4 6/2 * \
        |324 - 3/4 - 1/4 8/2 - 3/4 - 1/4 7/2 \
        |343 - 28/2 + 6/2 - 3/2 \
        |380 \
    ', 1/2)
    ns.pedal_pft(p, t0)

def main():
    do_20 = False
    do_118 = True
    do_212 = True
    do_300_1 = False
    do_118_rep = False
    do_212_rep = False
    do_300_2 = False
    
    ns = Score()
    # must make copies first; append_score() changes note times
    lh_118_211_copy = copy.deepcopy(lh_118_211)
    rh_118_211_copy = copy.deepcopy(rh_118_211)
    lh_212_299_copy = copy.deepcopy(lh_212_299)
    rh_212_299_copy = copy.deepcopy(rh_212_299)
    if do_20:
        t_20 = ns.cur_time
        ns.append_score([lh_20_117, rh_20_117])
    if do_118:
        t_118 = ns.cur_time
        ns.append_score([lh_118_211, rh_118_211])
    if do_212:
        t_212 = ns.cur_time
        ns.append_score([lh_212_299, rh_212_299])
    if do_300_1:
        t_300_1 = ns.cur_time
        ns.append_score([rh_300_307, lh_300_307])
    if do_118_rep:
        t_118_rep = ns.cur_time
        ns.append_score([lh_118_211_copy, rh_118_211_copy])
    if do_212_rep:
        t_212_rep = ns.cur_time
        ns.append_score([lh_212_299_copy, rh_212_299_copy])
    if do_300_2:
        t_300_2 = ns.cur_time
        ns.append_score([rh_300_end, lh_300_end])
        #ns.append_score([lh_300_end])

    ns.set_tempo(144)

    # pedal control
    if do_20:
        p20_117(ns, t_20)
    if do_118:
        p118_211(ns, t_118)
    if do_212:
        p212_299(ns, t_212)
    if do_300_1:
        p300_1(ns, t_300_1)
    if do_118_rep:
        p118_211(ns, t_118_rep)
    if do_212_rep:
        p212_299(ns, t_212_rep)
    if do_300_2:
        p300_end(ns, t_300_2)
    
    ns.done()

    # other nuance
    if do_20:
        v20_117(ns, t_20)
        t20_117(ns, t_20)
    if do_118:
        v118_211(ns, t_118)
        t118_211(ns, t_118)
    if do_212:
        v212_299(ns, t_212)
        t212_299(ns, t_212)
    if do_300_1:
        v300_1(ns, t_300_1)
        t300_1(ns, t_300_1)
    if do_118_rep:
        v118_211(ns, t_118_rep)
        t118_211(ns, t_118_rep)
    if do_212_rep:
        v212_299(ns, t_212_rep)
        t212_299(ns, t_212_rep)
    if do_300_2:
        v300_end(ns, t_300_2)
        t300_end(ns, t_300_2)

    ns.perf_dur_rel(.5, lambda n: 'stac' in n.tags)
    ns.t_random_normal(.008, 2)
    print(ns)
    ns.write_midi('data/app57.midi')
    pianoteq.play('data/app57.midi')

main()
