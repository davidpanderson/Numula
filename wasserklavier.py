from note import *
from notate import *
from nuance import *

def set_vol(ns):
    vol_seg(ns, ppp, mp, 18/8)
    vol_seg(ns, mp, pp, 12/8)
    vol_seg(ns, pp, ppp, 18/8)
    vol_seg(ns, pp, mp, 18/8)
    
    vol_adjust(ns, .7, lambda n: 'highest' not in n.tags and 'lowest' not in n.tags)
    vol_adjust(ns, .9, lambda n: 'highest' not in n.tags and 'lowest' in n.tags)

def set_tempo(ns):
    tempo_seg(ns, 18/8, linear, [60,80])
    tempo_seg(ns, 12/8, linear, [80,50])
    tempo_seg(ns, 36/8, linear, [50,70])
    
def main():
    rh1 = n('3/16 .  ++d- 2/8 c 1/8 +c \
        3/8 -f [c -c] \
        3/16 [e- -g] ++d- 2/8 [c -f] 1/8 ++c \
        3/16 [5/8 -f 3/8 -g] +d- 2/8  [c a-] 1/8 ++c \
        3/16 -f d- [c -e-] ++c \
        ')
    rh2 = n(' 3/16 [+c e-] [d- f] d- e- 1/4 c 1/8 c \
        3/16 [-e- +b-] +b- [--f b- +a-] [d- --b-] 1/4 [c 3/8 +g-] 1/8 -c \
        3/16 [--f +c f] +f [b- f -b-] -e- [a- d- f 1/4 a-] --d- 1/8 _ +a- \
        3/16 [c 3/8 d- g-] -b- d- +c [d- -d- 3/8 g-] [e- +e-] \
        ')
    rh3 = n(' 3/16 [++e- 3/8 f -b- f] [+d- +d-] [e- -f c a- f] +++f 1/4 [--f b-] 1/8 [e- -e-] \
        3/16 [--f b- +g-] [+f +f] 1/8 . 1/32 _ 1/64 ----c +c 1/8 [c +c] [-c -c] \
        3/16 [f +e-] c [+c +c] \
        1/32 _ 1/64 ---f +f 3/16 [f +f] +f ---c [+g- +g-] \
        ')
    lh1 = n('6/8 . 2/8 [--f +c +a-] 1/8 [-d- +b-] 2/8 [--f +e-] 1/8 [f +d-] \
        3/8 --f  [f ++a-] \
        [--f ++b-] [--f ++c] \
        [--f ++b-] 3/16 --f [++f +d-] \
        ')
    lh2 = n('3/8 [-g- --f] [+f b- ---f] [+f +e-] \
        -g- f e- \
        d- c b- \
        1/4 e- 1/8 f 1/4 [g- ++b-] 1/8 --a- 3/8 [a ++c] \
        ')
    lh3 = n(' 3/8 [b- -b-] 3/16 [c +a-] [d- -d-] 1/4 [c +g-] 1/8 [-c +c] \
        3/8 [b- f -b-] [a- +a-] \
        3/16 [g- -g-] ++b- 1/4 c 1/8 [c +c] \
        3/16 [---f +f] ++d- 3/8 [--e- -e-] \
        ')

    ns = NoteSet()
    #ns.append_ns([rh1, lh1])
    #ns.append_ns([rh2, lh2])
    ns.append_ns([rh3])
    ns.done()
    #set_vol(ns)
    #set_tempo(ns)
    ns.print()
    ns.write_midi('wasserklavier.midi')

main()
