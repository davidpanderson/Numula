# Robert Helps: Hommage a Ravel

from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

soprano = sh_score('meas3/4 \
    |1 <*3 1/2 1/4 * 3/4> f6 e f c f e d- \
    |5 f e f d- f e c \
    |9 f g a g+ e g d \
    |13 f+ g+ a g e e- -b \
    |17 [g +e] [d+ -f+] [g +e] [f+ -f+] [++a --g+] [a d] [ f -g] \
    |21 [g +e-] [d- a-] [g +e-] [e -f] [g ++a-] [f+ -g+] [f+ +c+] \
    |25 [c +b] [c -f] [c +b] [g+ -c+] [c ++c+] [c -f] [g+ -c+ ] \
    |29 [c +b-] [a -d] [c+ f+] [d c] [a +g] [f -f+] [b -c] \
    |33 f6 e f d- f e c \
    |37 f e f c f e d- \
    |41 f g a e g+ g d \
    |45 f+ g+ a g e b e- \
    |49 [e -g] [f+ +d+] [e -g] [f+ +f+] [a --g+] [a d] [f -g] \
    |53 [g +e-] [d- a-] [g +e-] [e -f] [g ++a-] [f+ -g+] [f+ +c+] \
    |57 [c +b] [c -f] [-c +b] [g+ -c+] [c ++c+] [c -f] [g+ -c+] \
    |61 [c6 +b-] [a -d] [c+ f+] [d c] [a +g] [f -f+] [b -c+] \
    |65 3/4 . . \
    |67 <*3 1/2 1/4 * 3/4> \
        [g6 +e] [d+ -f+] [g +e] [f+ -f+] [g+ ++a] [-d a] [g +f] \
    |71 [e- -g] [a- d-] [e- -g] [f +e] [a- --g] [g+ +f+] [c+ -f+] \
    |75 [+c +b] [c -f] [+b -c] [c+ +g+] [c+ --c] [f +c] [g+ -c+] \
    |79 [c +b-] [a -d] [c+ +f+] [d c] [a +g] [f -f+] [-c +b] \
    |83 1/2 [-c +b] [-c +b] 5/4 [-c +b] \
    |86 \
')

alto = sh_score('meas3/4 \
    |1 1/8 . e6 e c . -f . +e e d- . -f . +e -f +e . c  . e e c+ e -f \
    |5 . +e c -f . +d- . e e c . -f . f +c e . f . e d- -f f +e \
    |9 . e c c . -f . +e d- c . -f . +e- c +g . --f . +e c c +g --f \
    |13 . +e d -f . +e . g+ e -f . +c . d- e- -f . ++g . g+ f+ d+ c -f \
    |17 *2 \
        1/12 . [b6 +g+] [f+ c+] [d+ -f+] [+b -c] f . [g +d] [c f] \
        . [f+ -g+] [b- +f] [d -e] [f+ +c] [g d] . [f b-] [g c] \
        . [b +g+] [f+ c+] [d+ -f+] [g +c+] [a -d] . [f+ b] [g+ +d+] \
        . [f+ -g+] [b- +f] [-b -e+] [f+ g+] [f+ +c+] [e -g+] [f +f] [d -g] \
        * \
    |25 *2 \
        . [b6 +b-] [a g+] [f+ -g+] [b- +f] [-b -f] . [+f b] [g -b ] \
        . [b6 +b-] [a g+] [f+ -g+] [b- +f] [-b -f] . [+c+ f+] [f -g] \
        . [a +g+] [g -b] [f +e] [d -g] [a -d] . [g +f+] [c+ b+] \
        . [c +g] [a --g] [g+ +f+] [-c+ b+] [ g +f] [g -c+] [g+ ++a] [f+ -b] \
        * \
    |33 1/12 . c6 d- 1/8 d- -f . [b ++c] 1/12 . -e c d- -f ++b 1/8 . -c \
    |35 1/12 . e b e c+ +c 1/8 . [-f -f] 1/12 . +e d- e -f +c +b -d- f \
    |37 *2 \
        1/12 . e c d- -f +c 1/8 . [c +b] 1/12 . -e c 1/8 e [-f ++c] 1/12 . b -d- \
        . e e c -f ++g 1/8 . [b -b] 1/12 . +f e +c --f +e +c --b e \
        * \
    |45 1/12 . c6 d- 1/8 d- -f . [b ++c] 1/12 . -e c d- -f ++b 1/8 . -c \
    |47 1/12 . e b e c+ +c 1/8 . [-f -f] 1/12 . +e d- e -f +c +b -d- f \
    |49 1/12 . 1/36 g7+ -b +g+ -c+ f+ c+ d+ -f+ +d+ b -c +b \
        1/12 f . 1/36 +d -g +d c f c \
    |50 1/12 . 1/36 g6+ +f+ -g+ b- +f -b- -e +d -e +c -f+ +c -d g d \
        1/12 . 1/36 f b- f +c g c \
    |51 1/12 . 1/36 g7+ -b +g+ f+ c+ f+ d+ -f+ +d+ -g +c+ -g a -d +a \
        1/12 . 1/36 f+ b f+ g+ +d+ -g+ \
    |52 1/12 . 1/36 f7+ -g+ +f+ f -b- +f -b -e+ +b f+ g+ f+ \
        +c+ -f+ +c+ g+ +e -g+ +f -f +f d -g +d \
    |53 1/12 . 1/36 b6 +g+ -b +f+ c+ f+ -f+ +d+ -f+ -c +b -c \
        1/12 f . 1/36 g +d -g +f c f \
    |54 1/12 . 1/36 f+ -g+ +f+ f -b- +f d -e +d -f+ +c -f+ g d g \
        1/12 . 1/36 b- f b- g c g \
    |55 1/12 . 1/36 b6 +g+ -b c+ f+ c+ -f+ +d+ -f+ +c+ -g +c+ -d +a -d \
        1/12 . 1/36 +b f+ b d+ -g+ +d+ \
    |56 1/12 . 1/36 -g+ +f+ -g+ b- +f -b- -e+ +b -e+ g+ f+ g+ \
        f+ +c+ -f+ +e -g+ +e -f +f -f g +d -g \
    |57 1/12 . 1/48 b7- -b +b- -b +a g+ a g+ g+ +f+ -g+ +f+ -b- +f -b- f+ \
        -f +b -f +b 1/12 . 1/48 b -f +b -f +b +g -b +g \
    |58 1/12 . 1/48 b6 +b- -b +b- g+ ++a --g+ ++a f+ -g+ +f+ -g+ +f -b- +f -b- \
        b f b f 1/12 . 1/48 c+ f+ c+ f+ g +f -g +f \
    |59 1/12 . 1/48 a6 +g+ -a +g+ -b +g -b +g f +e -f +e -g +d -g +d \
        a -d +a -d 1/12 . 1/48 g +f+ -g +f+ c+ b+ c+ b+ \
    |60 1/12 . 1/48 c6 +g -c +g g ++a --g ++a --g+ +f+ -f +f+ c+ b+ c+ b+ \
        +f -g +f -g g -c+ +g -c+ +a --g+ ++a --g+ +f+ b f+ b \
    |61 1/12 . 1/24 b7- -b +a g+ f+ -g+ +f -b- b -f 1/12 . 1/24 ++b -f g -b \
    |62 1/12 . 1/24 +b- -b +a g+ f+ -g+ +f -b- b -f 1/12 . 1/24 ++f+ c+ +f -g \
    |63 1/12 . 1/24 g7+ -a +g -b e -f +d -g a -d 1/12 . 1/24 ++f+ -g +c+ c \
    |64 1/12 . 1/24 +g -c +a --g +f+ -g+ c+ c f -g +g -c +a --g+ +f+ -b \
    |65 1/12 . 1/24 g7 -c +a --g +f+ -g+ c+ c f -g +g -c +a --g+ +f+ -b \
    |66 1/12 . [c +g] [a --g] [g+ +f+] 1/6 [c+ b+] 1/8 [c +g] [a --g+] \
    |67 1/12 *2 \
        . [b6 +g+] [f+ c+] [d+ -f+] [b -c] f . [g +d] [c f] \
        . [f+ -g+] [b- +f] [d -e] [f+ +c] [g d] . [f b-] [g c] \
        . [b +g+] [f+ c+] [d+ -f] [g +c+] [a -d] . [f+ b] [g+ +d+] \
        . [f+ -g+] [b- +f] [-b -e+] [f+ g+] [f+ +c+] [e -g+] [f +f] [d -g] \
        * \
    |75 *2 \
        . [b6 +b-] [a g+] [f+ -g+] [b- +f] [-b -f] . [+f +b] [g -b] \
        . [b6 +b-] [a g+] [f+ -g+] [b- +f] [-b -f] . [+c+ f+] [f -g] \
        . [a +g+] [g -b] [-f +e] [d -g] [a -d] . [g +f+] [-c+ b+] \
        . [c +g] [a --g] [g+ +f+] [c+ b+] [g +f] [g -c+] [g+ ++a] [f+ -b] \
        * \
    |83 . [c +g] [a --g] [g+ +f+] [c+ b+] . . [c +g] [a --g] \
    |84 . . . . [c +g] . . . . 3/4 [c8+ --c] \
    |86 \
')

# various off-beat notes
tenor = sh_score('meas3/4 \
    |1 3/4 *31 . * \
    |32 1/4 . . c6 \
    |33 3/4 *24 . * \
    |57 1/12 . f6 e f c . . . . \
    |58 *2 . f e f d- . . . . * \
    |60 . f e 1/8 f c . . \
    |61 *2 3/16 . 5/16 e 1/4 . * \
    |63 3/4 . 3/8 . c+ \
    |65 2/4 . 1/16 . 3/16 c+ 1/4 . 1/8 . c+ 1/12 . 2/12 c+ \
    |67 1/8 . e6 e c . -f . +e e d- . -f . +e -f +e . c . e e c+ e -f \
    |71 . +e c -f . +d- . e e c . -f . f +c e . f . e d- -f f +e \
    |75 . e c c . -f . +e d- c . -f . +e- c +g . --f . +e c c +g --f \
    |79 . +e d -f . +e . g+ e -f . +c . d- e- -f . ++g . g+ f+ d+ c -f \
    |83 . ++g+ f+ d+ . g+ f+ d+ . g+ 1/4 f+ 3/4 d+ \
    |86 \
')

# the lower melody notes from m67 onward
bass = sh_score('meas3/4 \
    |1 3/4 *66 . * \
    |67 <*3 1/2 1/4 * 3/4> \
        f6 e f c f e d- \
    |71 f e f d- f e c \
    |75 f g a g+ e g d \
    |79 f+ g+ a g e e- b \
    |83 2/4 b b 5/4 b \
    |86 \
')

ped = sh_pedal('meas3/4 \
    |1 + 48/4 \
    |17 *4 \
        *4 + 2/4 + 1/4 * - \
        * \
    |33 + 48/4 \
    |49 *16 + 2/4 + 1/4 * \
    |65 + 6/4 \
    |67 *16 +2/4 + 1/4 * \
    |83 + 9/4 - \
    |86 1/4 - \
')

soprano_v0 = sh_vol('meas3/4 \
    |1 *2 [ mp 12/4 mp [ p 12/4 p * \
    |17 [ _p 12/4 _p [ pp 12/4 pp [ mf 12/4 mf [ p 12/4 p \
    |33 [ mp 48/4 mp \
    |49 [ p 24/4 p \
    |57 [ f 12/4 f \
    |61 [ p 9/4 p [ mf 9/4 f \
    |67 [ pp 48/4 pp \
    |83 [ pp 9/4 pp \
    |86 \
')

alto_v0 = sh_vol('meas3/4 \
    |1 ppp 48/4 ppp \
    |17 [ ppp 12/4 ppp [ _ppp 12/4 _ppp [ p 12/4 p [ _pp 12/4 _pp \
    |33 [ pppp_ 48/4 pppp_ \
    |49 [ ppp 24/4 ppp \
    |57 [ f 12/4 f \
    |61 [ pp 12/4 pp 3/4 pp [ p 3/4 pp \
    |67 [ ppp 36/4 ppp \
    |79 ppp 12/4 ppp 9/4 pppp \
    |86 \
')

a5 = 1.4
a4 = 1.3
a3 = 1.1
a2 = 1.0
a1 = .9

alto_v1 = sh_accents(f' \
    |1 *48 1. 1/4 {a4} 1/4 {a4} 1/4 * \
    |49 *12 *3 {a5} 1/12 {a4} 1/12 {a4} 1/12 * * \
    |61 \
')

tenor_v0 = sh_vol('meas3/4 \
    |1 *31 mm 3/4 mm * \
    |32 [ p 3/4 p \
    |33 *24 [ mm 3/4 mm * \
    |57 [ f 12/4 f \
    |61 [ p 9/4 p [ ff 3/4 ff \
    |65 [ pp 6/4 p \
    |67 [ ppp 48/4 ppp \
    |83 [ ppp 9/4 ppp \
    |86 \
')

bass_v0 = sh_vol('meas3/4 \
    |1 *66 mm 3/4 mm * \
    |67 [ mp 12/4 mp [ p 12/4 p [ mf 12/4 mf [ mp 12/4 pp \
    |83 pp 9/4 pp \
    |86 \
')

t0 = sh_tempo('meas3/4 \
    |1 *16 60 6/4 68 6/4 55 * \
    |65 55 6/4 30 \
    |67 *4 60 6/4 68 6/4 55 * \
    |83 55 9/4 30 \
    |86 \
')

dt0 = .03
dt1 = .05
dt2 = .08
dt3 = .11
dt4 = .14

t1 = sh_tempo(f'meas3/4 \
    |1 *16 {dt3}p{dt2} 6/4 . {dt2}p{dt1} 6/4 . * \
    |65 6/4 . .3p \
    |67 *4 {dt3}p{dt2} 6/4 . {dt2}p{dt1} 6/4 . * \
    |83 \
')

nuance = True

def main():
    ns = Score(tempo=72)
    if nuance:
        soprano.vol_adjust_pft(soprano_v0)
        alto.vol_adjust_pft(alto_v0)
        alto.vol_adjust_pft(alto_v1)
        tenor.vol_adjust_pft(tenor_v0)
        bass.vol_adjust_pft(bass_v0)
    ns.append_scores([
        soprano,
        alto,
        tenor,
        bass
    ])
    if nuance:
        ns.pedal_pft(ped)
        ns.tempo_adjust_pft(t0)
        ns.tempo_adjust_pft(t1)
    #print(ns)
    numula.pianoteq.play_score(ns)
    #numula.read_midifile.print_midifile(fname)
main()
