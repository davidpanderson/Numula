# Aria from Bach's Goldberg variations
# It's mostly 3 voices (soprano/tenor/bass)
# Occasionally there's a 4th voice, which I'll call alto.

# It's two 16-measure sections, each of which is repeated.
# The ornaments and nuance can differ between the repeats

import numula_path
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

def soprano1(first):
    return sh_score('meas3/4 \
    |1 1/4 g6 g 3/16 orn[a g a 1/20] 1/16 (short b short) \
    |2 1/8 a orn[g f+ 1/16] 1/2 orn[e d 1/8 ] \
    |3 1/4 orn[g5 f+ g 1/16] 3/8 orn[a g f+ *6 g a * g 3/8] 1/16 f+ g \
    |4 1/32 a g 1/16 f+ 1/32 g f+ 1/16 e 1/2 orn[e d 1/8 tag=app] \
    |5 1/4 +d d 3/16 orn[e d e 1/16] 1/16 (short f short) \
    |6 1/8 e orn[d c 1/16] 3/8 orn[b a 1/8 tag=app] 1/8 orn[g6 f+ e f+ 1/8] \
    |7 <1/32 3/32> g f+ a g f+ e d c 3/16 orn[c +a 1/16] 1/16 -c \
    |8 1/32 b 3/32 g 1/8 f+ 1/4 f+ 1/4 orn[g f+ g 1/16] \
    |9 1/4 b b 3/16 orn[c+ b c+ 1/16] 1/16 (short d short) \
    |10 d c+ b 9/16 a 1/2 _ d6 \
    |11 1/4 [g5 b e g] 3/8 orn[a g f+ g *3 a g * f+ g 1/4] 1/16 f+ g \
    |12 1/8 g orn[f+ e 1/16] 3/8 orn[d6 c+ b c+ *3 d c+ * b c+ 1/4] 1/8 e \
    |13 1/16 a g f+ e 1/8 d 9/32 a 1/32 b 1/16 c \
    |14 1/16 b a g f+ 1/8 e 9/32 orn[+d c+ 1/16] 1/32 d 1/16 e \
    |15 1/16 d c+ b a 1/8 +g 1/4 -b 1/8 c+ \
    |16 5/32 orn[c+ d 1/16] 1/32 e d c+ 1/2 orn[c+ d 1/4] \
    |17 \
    ').tag('soprano')

def soprano2(first):
    return sh_score('meas3/4 \
    |17 1/4 orn[a5 g a 1/20] 5/16 orn[b a g a *3 b a * 1/5] 1/32 a b c d 1/16 e \
    |18 1/8 orn[e d 1/16] orn[c b 1/16] 3/8 orn[a g 1/16] 1/8 g6 \
    |19 3/16 orn[f+ e 1/16] 1/32 f+ d+ 1/8 d+ 1/4 orn[e d+ e 1/20] 1/32 a b a g \
    |20 3/16 a 1/16 f+ 3/8 orn[e d+ 1/16] 1/8 b \
    |21 3/16 orn[e f+ g 1/16] 1/16 f+ 5/16 orn[f+ e 1/18] 1/16 b 1/32 c b a b \
    |22 1/32 g6 3/32 e 1/32 f+ 3/32 d+ 5/16 orn[d+ e 1/16] 1/16 g5 f+ e \
    |23 3/16 f+ 1/16 e6 1/8 orn[e d+ 1/16] orn[f+ g a 1/16] g f+ \
    |24 3/16 orn[f+ e 1/16] 1/32 f+ d+ 1/2 orn[d+ e 1/10 ] \
    |25 1/8 e orn[d c 1/16] 3/8 orn[b a 1/8] 1/16 b c \
    |26 1/32 d c 1/16 b 1/32 c b 1/16 a 3/8 orn[a g 1/16] 1/16 a b \
    |27 c d c b c a e a 5/16 c 1/16 _ \
    |28 1/16 . d c b c a f+ a c e d c \
    |29 b c b a b g d g b g c d \
    |30 e f e d e c g c e c +f+ g \
    |31 a -c b a b c d -g b a g f+ \
    |32 5/16 g 1/16 d g f+ 1/4 orn[f+ g 1/8 ] \
    |33 \
    ').tag('soprano')

def alto1(first):
    return sh_score('meas3/4 \
    |1 1/4 . . d5 . . d . . c+ . . a \
    |5 . . g . . a 3/4 . . \
    |9 1/4 . . +e 3/4 . . . \
    |13 1/4 . . d5 3/4 . . 3/8 . 1/8 a 1/4 d \
    |17 \
    ').tag('alto')

def alto2(first):
    return sh_score('meas3/4 \
    |17 3/4 *6 . * \
    |23 5/8 . 1/8 d4+ 1/4 e . . \
    |25 1/4 . 1/2 e4 \
    |26 \
    ').tag('alto')

def tenor1(first):
    return sh_score('meas3/4 \
    |1 <1/4 1/2> . b4 . a . g . f+ \
    |5 . d 1/4 . 3/8 e 1/8 . \
    |7 1/8 . 2/8 c5 1/16 b a g f+ e f+ 1/8 g a 1/2 b \
    |9 1/4 . 1/2 b 1/4 a . . \
    |11 1/8 . b 3/8 e 1/8 d c+ d 1/2 e \
    |13 1/4 . 1/2 a4 1/4 . b e f+ 3/16 e 1/16 f+ 1/2 g f+ \
    |17 \
    ').tag('tenor')

def tenor2(first):
    return sh_score('meas3/4 \
    |17 1/8 . e5 1/2 orn[f+ e f+ 1/8] 1/8 . c5 1/2 d \
    |19 1/8 . e 1/4 g 1/8 orn[g f+ g f+ 1/16] e \
    |20 d+ e 1/2 f+ \
    |21 1/8 . a4 orn[a g a g 1/16] f+ 1/4 g \
    |22 1/8 . a orn[a g a g 1/16] f+ g b \
    |23 3/8 f5+ 1/8 +c b 3/8 a 1/2 g \
    |25 1/2 . 3/8 a4 1/8 f+ 1/8 orn[e d 1/16] 1/16 e f+ g f+ 1/4 g 1/8 _ \
    |27 1/8 . e a 3/16 +e 1/16 b5 a g \
    |28 1/4 f+ 1/8 . 3/8 f+ 1/8 g . . 3/16 d 7/16 g 1/4 _ \
    |30 3/8 . 3/16 g c 3/4 . 1/16 . c5 b a 1/2 b \
    |33 \
    ').tag('tenor')

def bass1(first):
    return sh_score('meas3/4 \
    |1 3/4 g4 f+ e 5/8 d 1/8 c \
    |5 3/4 b 5/8 c 1/8 d \
    |7 e c 1/2 d 3/8 -g 1/8 +d 3/16 orn[e d e 1/16] 1/16 f+ \
    |9 4/4 g 1/8 orn[g f+ g f+ 1/16] e f+ b \
    |11 3/8 -e 1/8 e f+ g 3/8 a 1/8 b a g \
    |13 3/4 f+ g a -d \
    |17 \
    ').tag('bass')

def bass2(first):
    return sh_score('meas3/4 \
    |17 1/2 d5 1/4 c 3/8 b 1/8 a 1/4 b \
    |19 3/8 c 1/8 b 1/4 a 3/8 b 1/8 a g f+ \
    |21 1/2 e 1/4 d 1/2 c 1/4 b \
    |23 1/8 a c b a 1/4 b 1/8 e b -e +b e d \
    |25 3/4 c b \
    |27 3/8 a 1/8 g f+ e d +a d c b a \
    |29 g +d g f e d c +g c b a g \
    |31 f+ d g b d -d 3/8 g 1/8 d 1/4 -g \
    |33 \
    ').tag('bass')

# volume, accents

soprano_v0 = sh_vol('meas3/4 \
    |1 p_ 3/4 _mf \
    |2 [ mf_ 1/8 mf_ [ mp 1/8 mm 1/2 p_ \
    |3 [ p_ 1/4 p 2/4 mm \
    |4 [ mm 3/4 pp \
    |5 [ mp 3/4 mf 3/8 mm 3/8 mf \
    |7 [ mf 2/4 _f 1/4 mf 3/4 p \
    |9 [ mm 24/4 mm \
    |17 \
')

alto_v0 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

tenor_v0 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

bass_v0 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

# accent appogiaturas
def accent_apps(ns):
    for orn in filter(lambda x: len(x.notes) == 1, ns.ornaments):
        for n in orn.notes:
            ns.vol_adjust(1.1, n)

# tempo, pauses

tempo0 = sh_tempo('meas3/4 \
    |1 50 3/4 65 3/4 55 \
    |3 60 3/4 50 60 3/4 50 \
    |5 55 3/4 65 3/4 55 \
    |7 65 6/4 55 \
    |9 60 3/4 65 3/4 55 \
    |11 60 6/4 55 \
    |13 60 12/4 50 \
    |17 \
')

# shorten tagged 16ths
#
def shorten_16ths(ns):
    ns.start_adjust(1/50, lambda n: 'short' in n.tags)

dt0 = .03
dt1 = .05
dt2 = .08
dt3 = .11
dt4 = .14
dt5 = .18
dt6 = .23
dt7 = .29

pauses = sh_tempo(f'meas3/4 \
    |1 11/16 . {dt7}p 1/16 . 3/4 . {dt3}p \
    |3 3/4 . {dt0}p 1/8 . {dt0}p 1/8 . {dt0}p 2/4 . {dt4}p \
    |5 11/16 . {dt2}p 1/16 . 5/8 . {dt3}p 1/8 . \
    |7 2/4 . {dt1}p 1/4 . 11/16 . {dt3}p 1/16 . \
    |9 11/16 . {dt2}p 1/16 . 3/4 . {dt3}p \
    |11 6/4 . \
    |13 *4 2/4 . p{dt3} 1/4 . * \
    |17 \
')

def nuance1(ns):
    accent_apps(ns)
    shorten_16ths(ns)
    ns.tempo_adjust_pft(tempo0)
    ns.tempo_adjust_pft(pauses)
    
    x = sh_tempo('40 1/2 80 1/4 40')
    pft_scale_dur(x, 2/4)
    ns.tempo_adjust_pft(x, 7/4, lambda n: 'soprano' in n.tags, True)
    ns.adjust_dur_rel(0.9,
        lambda n: 'soprano' in n.tags and 'orn' not in n.tags
    )
    ns.adjust_dur_rel(1.2,
        lambda n: 'soprano' in n.tags and 'orn' in n.tags
    )
    ns.slur('slur', lambda n: 'soprano' in n.tags, 1.2)
    ns.roll(30/4, roller(4, 0, .3), False, lambda n: 'soprano' in n.tags)

def nuance2(ns):
    pass

def main():
    ns = Score(tempo=55)
    do_nuance = True
    for first in [True, False]:
        s = soprano1(first)
        a = alto1(first)
        t = tenor1(first)
        b = bass1(first)
        if do_nuance:
            s.vol_adjust_pft(soprano_v0)
            a.vol_adjust_pft(alto_v0)
            t.vol_adjust_pft(tenor_v0)
            b.vol_adjust_pft(bass_v0)
        ns1 = Score(tempo=55)
        ns1.append_scores([s, a, t, b])
        if do_nuance:
            nuance1(ns1)
        ns.append_score(ns1)
    for first in [True, False]:
        s = soprano2(first)
        a = alto2(first)
        t = tenor2(first)
        b = bass2(first)
        if False:
            s.vol_adjust_pft(soprano_v0)
            a.vol_adjust_pft(alto_v0)
            t.vol_adjust_pft(tenor_v0)
            b.vol_adjust_pft(bass_v0)
        ns2 = Score(tempo=55)
        ns2.append_scores([s, a, t, b])
        if do_nuance:
            nuance1(ns2)
        ns.append_score(ns2)

    #print(ns)
    numula.pianoteq.play_score(ns)

main()
