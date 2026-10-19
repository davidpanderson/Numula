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
    |1 1/4 g5 g 3/16 orn[a g a 1/24] 1/16 (short b short) \
    |2 1/8 a orn[g f+ 1/16] 1/2 orn[e d 1/8 ] \
    |3 1/4 orn[g4 f+ g 1/24] 3/8 orn[a g f+ *6 g a * g 3/8] 1/16 f+ g \
    |4 1/32 a g 1/16 f+ 1/32 g f+ 1/16 e 1/2 orn[e d 1/8 tag=app] \
    |5 1/4 +d d 3/16 orn[e d e 1/20] 1/16 (short f short) \
    |6 1/8 e orn[d c 1/16] 3/8 orn[b a 1/8 tag=app] 1/8 orn[g5 f+ e f+ 1/8] \
    |7 <1/32 3/32> g f+ a g f+ e d c 3/16 orn[c +a 1/16] 1/16 -c \
    |8 1/32 b 3/32 g 1/8 f+ 1/4 f+ 1/4 orn[g f+ g 1/20] \
    |9 1/4 b b 3/16 orn[c+ b c+ 1/20] 1/16 (short d short) \
    |10 d c+ b 9/16 a 1/2 _ d6 \
    |11 1/4 [g4 b e g] 3/8 orn[a g f+ g *3 a g * f+ g 1/4] 1/16 f+ g \
    |12 1/8 g orn[f+ e 1/16] 3/8 orn[d5 c+ b c+ *3 d c+ * b c+ 1/4] 1/8 e \
    |13 1/16 a g f+ e 1/8 d 9/32 a 1/32 b 1/16 c \
    |14 1/16 b a g f+ 1/8 e 9/32 orn[+d c+ 1/16] 1/32 d 1/16 e \
    |15 1/16 d c+ b a 1/8 +g 1/4 -b 1/8 c+ \
    |16 5/32 orn[c+ d 1/16] 1/32 e d c+ 1/2 orn[c+ d 1/4] \
    |17 \
    ').tag('soprano')

def soprano2(first):
    return sh_score('meas3/4 \
    |17 1/4 orn[a4 g a 1/24] 5/16 orn[b a g a *3 b a * 1/6] 1/32 a b c d 1/16 e \
    |18 1/8 orn[e d 1/16] orn[c b 1/16] 3/8 orn[a g 1/4] 1/8 g5 \
    |19 3/16 orn[f+ e 1/16] 1/32 f+ d+ 1/8 d+ 1/4 orn[e d+ e 1/20] 1/32 a b a g \
    |20 3/16 a 1/16 f+ 3/8 orn[e d+ 1/16] 1/8 b \
    |21 3/16 orn[e f+ g 1/16] 1/16 f+ 5/16 orn[f+ e 1/18] 1/16 b 1/32 c b a b \
    |22 1/32 g5 3/32 e 1/32 f+ 3/32 d+ 5/16 orn[d+ e 1/16] 1/16 g4 f+ e \
    |23 3/16 f+ 1/16 e5 1/8 orn[e d+ 1/16] orn[f+ g a 1/16] g f+ \
    |24 3/16 orn[f+ e 1/16] 1/32 f+ d+ 1/2 orn[d+ e 1/4 ] \
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
    |1 1/4 . . d4 . . d . . c+ . . a \
    |5 . . g . . a 3/4 . . \
    |9 1/4 . . +e 3/4 . . . \
    |13 1/4 . . d5 3/4 . . 3/8 . 1/8 a 1/4 d \
    |17 \
    ').tag('alto')

def alto2(first):
    return sh_score('meas3/4 \
    |17 3/4 *6 . * \
    |23 5/8 . 1/8 d3+ 1/4 e . . \
    |25 1/4 . 1/2 e3 \
    |26 \
    ').tag('alto')

def tenor1(first):
    return sh_score('meas3/4 \
    |1 <1/4 1/2> . b3 . a . g . f+ \
    |5 . d 1/4 . 3/8 e 1/8 . \
    |7 1/8 . 2/8 c4 1/16 b a g f+ e f+ 1/8 g a 1/2 b \
    |9 1/4 . 1/2 b 1/4 a . . \
    |11 1/8 . b 3/8 e 1/8 d c+ d 1/2 e \
    |13 1/4 . 1/2 a3 1/4 . b e f+ 3/16 e 1/16 f+ 1/2 g f+ \
    |17 \
    ').tag('tenor')

def tenor2(first):
    return sh_score('meas3/4 \
    |17 1/8 . e4 1/2 orn[f+ e f+ 1/8] 1/8 . c4 1/2 d \
    |19 1/8 . e 1/4 g 1/8 orn[g f+ g f+ 1/16] e \
    |20 d+ e 1/2 f+ \
    |21 1/8 . a3 orn[a g a g 1/16] f+ 1/4 g \
    |22 1/8 . a orn[a g a g 1/16] f+ g b \
    |23 3/8 f4+ 1/8 +c b 3/8 a 1/2 g \
    |25 1/2 . 3/8 a3 1/8 f+ 1/8 orn[e d 1/16] 1/16 e f+ g f+ 1/4 g 1/8 _ \
    |27 1/8 . e a 3/16 +e 1/16 b4 a g \
    |28 1/4 f+ 1/8 . 3/8 f+ 1/8 g . . 3/16 d 7/16 g 1/4 _ \
    |30 3/8 . 3/16 g c 3/4 . 1/16 . c4 b a 1/2 b \
    |33 \
    ').tag('tenor')

def bass1(first):
    return sh_score('meas3/4 \
    |1 3/4 g3 f+ e 5/8 d 1/8 c \
    |5 3/4 b 5/8 c 1/8 d \
    |7 e c 1/2 d 3/8 -g 1/8 +d 3/16 orn[e d e 1/16] 1/16 f+ \
    |9 4/4 g 1/8 orn[g f+ g f+ 1/16] e f+ b \
    |11 3/8 -e 1/8 e f+ g 3/8 a 1/8 b a g \
    |13 3/4 f+ g a -d \
    |17 \
    ').tag('bass')

def bass2(first):
    return sh_score('meas3/4 \
    |17 1/2 d4 1/4 c 3/8 b 1/8 a 1/4 b \
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

vol_soprano1 = sh_vol('meas3/4 \
    |1 _mf 3/4 mf \
    |2 [ _f 1/8 mf_ [ mp 1/8 mm 1/2 p_ \
    |3 [ mm 1/4 p 2/4 mf \
    |4 [ _mf 3/4 pp \
    |5 [ mp_ 3/4 mf 3/8 mm 3/8 mf \
    |7 [ mf 2/4 _f 1/4 mf 3/4 p \
    |9 [ _mf 3/4 mf 3/4 mp \
    |11 [ mm 3/4 mf 3/4 mp \
    |13 *3 [ _mf 2/4 mp 1/4 mf * \
    |16 [ mp 3/4 mf \
    |17 \
')

vol_soprano2 = sh_vol('meas3/4 \
    |17 mp 3/4 mf 3/4 mp \
    |19 [ mm 3/4 mf 3/4 mp \
    |21 [ mf 2/4 mp 1/4 mf \
    |22 3/4 mp \
    |23 3/4 mf \
    |24 3/4 p \
    |25 [ mm 3/4 p [ mm 3/4 p \
    |27 [ p 1/4 mm 2/4 p \
    |28 [ mp 1/4 _mf 2/4 mp \
    |29 [ mp_ 1/4 mf 2/4 mp \
    |30 [ mm 1/4 _mf 2/4 mf \
    |31 [ mf 3/4 mp \
    |32 [ mp 3/4 pp \
    |33 \
')

vol_alto1 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

vol_alto2 = sh_vol('meas3/4 \
    |17 p 48/4 p \
    |33 \
')

vol_tenor1 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

vol_tenor2 = sh_vol('meas3/4 \
    |17 p 30/4 p \
    |27 [ mm 3/4 mm \
    |28 15/4 mm \
    |33 \
')

vol_bass1 = sh_vol('meas3/4 \
    |1 p 48/4 p \
    |17 \
')

vol_bass2 = sh_vol('meas3/4 \
    |17 p 48/4 p \
    |33 \
')


# accent appogiaturas
def accent_apps(ns):
    for orn in filter(lambda x: len(x.notes) == 1, ns.ornaments):
        for n in orn.notes:
            ns.vol_adjust(1.1, n)

# tempo, pauses

tempo1 = sh_tempo('meas3/4 \
    |1 45 3/4 60 3/4 50 \
    |3 60 3/4 50 60 3/4 50 \
    |5 45 3/4 60 3/4 55 \
    |7 60 6/4 45 \
    |9 50 3/4 65 3/4 55 \
    |11 60 6/4 55 \
    |13 60 9/4 52 3/4 35 \
    |17 \
')

tempo2a = sh_tempo('meas3/4 \
    |17 45 3/4 60 3/4 50 \
    |19 55 3/4 60 3/4 55 \
    |21 55 3/4 60 3/4 60 \
    |23 60 6/4 50 \
    |25 55 18/4 60 6/4 50 \
    |33 \
')

tempo2b = tempo2a

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
dt8 = .35
dt9 = .4

pauses1 = sh_tempo(f'meas3/4 \
    |1 11/16 . {dt9}p 1/16 . {dt2}p 3/4 . {dt5}p \
    |3 5/8 . p{dt3} 1/8 . \
    |4 1/8 . {dt0}p 1/8 . {dt0}p 2/4 . {dt4}p \
    |5 11/16 . {dt8}p 1/16 . 5/8 . {dt3}p 1/8 . \
    |7 2/4 . {dt1}p 1/4 . 11/16 . {dt9}p 1/16 . \
    |9 11/16 . {dt8}p 1/16 . \
    |10 p{dt1} 3/4 . {dt3}p \
    |11 6/4 . \
    |13 *4 p{dt1} 2/4 . p{dt3} 1/4 . * \
    |17 \
')

pauses2a = sh_tempo(f'meas3/4 \
    |17 2/4 . p{dt2} 1/4 . {dt2}p \
    |18 11/16 . {dt3}p 1/16 . \
    |19 5/8 . {dt3}p 1/8 . \
    |20 {dt2}p 5/8 . {dt3}p 1/8 . \
    |21 2/4 . p{dt3} 1/4 . \
    |22 2/4 . p{dt2} 1/4 . \
    |23 3/8 . {dt3}p 3/8 . \
    |24 3/4 . \
    |25 {dt3}p 5/8 . {dt3}p 1/8 . \
    |26 3/4 . \
    |27 2/4 . {dt2}p 1/4 . \
    |28 2/4 . p{dt2} 1/4 . \
    |29 3/4 . \
    |30 3/4 . \
    |31 p{dt1} 2/4 . p{dt1} 1/4 . \
    |32 p{dt1} 1/4 . p{dt3} 2/4 . 1.p \
    |33 \
')

pauses2b = pauses2a

def timing1(ns, first, t):
    if first:
        ns.tempo_adjust_pft(tempo1, t)
        ns.tempo_adjust_pft(pauses1, t)
    else:
        ns.tempo_adjust_pft(tempo1, t)
        slower = sh_tempo('55 48/4 55')
        ns.tempo_adjust_pft(slower, t)
        ns.tempo_adjust_pft(pauses1, t)
    
    x = sh_tempo('40 1/2 80 1/4 40')
    pft_scale_dur(x, 2/4)
    ns.tempo_adjust_pft(x, t+7/4, lambda n: 'soprano' in n.tags, True)
    ns.roll(t+30/4, roller(4, 0, .3), False, lambda n: 'soprano' in n.tags)

def timing2(ns, first, t):
    if first:
        ns.tempo_adjust_pft(tempo2a, t)
        ns.tempo_adjust_pft(pauses2a, t)
    else:
        ns.tempo_adjust_pft(tempo2b, t)
        ns.tempo_adjust_pft(pauses2b, t)

# adjustments that apply throughout
#
def timing_all(ns):
    accent_apps(ns)
    shorten_16ths(ns)
    ns.adjust_dur_rel(0.9,
        lambda n: 'soprano' in n.tags and 'orn' not in n.tags
    )
    ns.adjust_dur_rel(1.2,
        lambda n: 'soprano' in n.tags and 'orn' in n.tags
    )
    ns.slur('slur', lambda n: 'soprano' in n.tags, 1.2)

def main():
    ns = Score(tempo=55)
    do_nuance = True
    for first in [True, False]:
        s = soprano1(first)
        a = alto1(first)
        t = tenor1(first)
        b = bass1(first)
        if do_nuance:
            s.vol_adjust_pft(vol_soprano1)
            a.vol_adjust_pft(vol_alto1)
            t.vol_adjust_pft(vol_tenor1)
            b.vol_adjust_pft(vol_bass1)
        ns1 = Score(tempo=55)
        ns1.append_scores([s, a, t, b])
        ns.append_score(ns1)
    for first in [True, False]:
        s = soprano2(first)
        a = alto2(first)
        t = tenor2(first)
        b = bass2(first)
        if do_nuance:
            s.vol_adjust_pft(vol_soprano2)
            a.vol_adjust_pft(vol_alto2)
            t.vol_adjust_pft(vol_tenor2)
            b.vol_adjust_pft(vol_bass2)
        ns2 = Score(tempo=55)
        ns2.append_scores([s, a, t, b])
        ns.append_score(ns2)

    if do_nuance:
        timing1(ns, True, 0)
        timing1(ns, False, 48/4)
        timing2(ns, True, 96/4)
        timing2(ns, False, 144/4)
        timing_all(ns)

    #print(ns)
    #numula.pianoteq.play_score(ns)
    numula.pianoteq.play_score(ns)

main()
