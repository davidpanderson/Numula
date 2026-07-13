# Aria from Bach's Goldberg variations
# It's mostly 3 voices (soprano/tenor/bass)
# Occasionally there's a 4th voice, alto.

import numula_path
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq

soprano = sh_score('meas3/4 \
    |1 1/4 g6 g 3/16 orn[10 g a b 1/20] 1/16 (short b short) \
    |2 1/8 a orn[2 - f+ g 1/16] 1/2 orn[2 - d e 1/8 ] \
    |3 1/4 orn[10 f5+ g a 1/16] 3/8 orn[210(12)1 f+ g a rep=6 3/8] 1/16 f+ g \
    |4 1/32 a g 1/16 f+ 1/32 g f+ 1/16 e 1/2 orn[2 - d e 1/8 tag=app] \
    |5 1/4 +d d 3/16 orn[ 10 d e 1/16] 1/16 (short f short) \
    |6 1/8 e orn[2 - c d 1/16] 3/8 orn[2 - a b 1/8 tag=app] 1/8 orn[2101 +e f+ g 1/8] \
    |7 <1/32 3/32> g f+ a g f+ e d c 3/16 orn[0 c +a 1/16] 1/16 -c \
    |8 1/32 b 3/32 g 1/8 f+ 1/4 f+ 1/4 orn[10 f+ g 1/16] \
    |9 1/4 b b 3/16 orn[10 b c+ d 1/16] 1/16 (short d short) \
    |10 d c+ b 9/16 a 1/2 _ d6 \
    |11 1/4 [g5 b e g] 3/8 orn[2101(21)0 f+ g a 1/4 rep=3] 1/16 f+ g \
    |12 1/8 g orn[2 - e f+ 1/16] 3/8 orn[2101(21)0 b5 c+ d 1/4 rep=3] 1/8 e \
    |13 1/16 a g f+ e 1/8 d 9/32 a 1/32 b 1/16 c \
    |14 1/16 b a g f+ 1/8 e 9/32 orn[2 - +c+ d 1/16] 1/32 d 1/16 e \
    |15 1/16 d c+ b a 1/8 +g 1/4 -b 1/8 c+ \
    |16 5/32 orn[0 c+ d 1/16] 1/32 e d c+ 1/2 orn[0 c+ d 1/8] \
    |17 \
').tag('soprano')

alto = sh_score('meas3/4 \
    |1 1/4 . . d5 . . d . . c+ . . a \
    |5 . . g . . a 3/4 . . \
    |9 1/4 . . +e 3/4 . . . \
    |13 1/4 . . d5 3/4 . . 3/8 . 1/8 a 1/4 d \
    |17 \
').tag('alto')

tenor = sh_score('meas3/4 \
    |1 <1/4 1/2> . b4 . a . g . f+ \
    |5 . d 1/4 . 3/8 e 1/8 . \
    |7 1/8 . 2/8 c5 1/16 b a g f+ e f+ 1/8 g a 1/2 b \
    |9 1/4 . 1/2 b 1/4 a . . \
    |11 1/8 . b 3/8 e 1/8 d c+ d 1/2 e \
    |13 1/4 . 1/2 a4 1/4 . b e f+ 3/16 e 1/16 f+ 1/2 g f+ \
    |17 \
').tag('tenor')

bass = sh_score('meas3/4 \
    |1 3/4 g4 f+ e 5/8 d 1/8 c \
    |5 3/4 b 5/8 c 1/8 d \
    |7 e c 1/2 d 3/8 -g 1/8 +d 3/16 orn[10 d e 1/16] 1/16 f+ \
    |9 4/4 g 1/8 orn[212 - f+ g 1/16] e f+ b \
    |11 3/8 -e 1/8 e f+ g 3/8 a 1/8 b a g \
    |13 3/4 f+ g a -d \
    |17 \
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
    ns.vol_adjust(1.1, lambda n: 'app' in n.tags)

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

def main():
    ns = Score(tempo=55)
    do_nuance = True
    if do_nuance:
        soprano.vol_adjust_pft(soprano_v0)
        alto.vol_adjust_pft(alto_v0)
        tenor.vol_adjust_pft(tenor_v0)
        bass.vol_adjust_pft(bass_v0)
    ns.append_scores([
        soprano,
        alto,
        tenor,
        bass
    ])
    if do_nuance:
        accent_apps(ns)
        shorten_16ths(ns)
        ns.tempo_adjust_pft(tempo0)
        ns.tempo_adjust_pft(pauses)
        
        x = sh_tempo('40 1/2 80 1/4 40')
        pft_normalize_dur(x, 2/4)
        ns.tempo_adjust_pft(x, 7/4, lambda n: 'soprano' in n.tags, True)
        ns.perf_dur_rel(0.9,
            lambda n: 'soprano' in n.tags and 'slur' not in n.tags and 'orn' not in n.tags
        )
        ns.slur('slur', lambda n: 'soprano' in n.tags, 1.2)
        ns.slur('orn', lambda n: 'soprano' in n.tags, 1.2)
        ns.roll(30/4, roller(4, 0, .3), False, lambda n: 'soprano' in n.tags)

    print(ns)
    #numula.pianoteq.play_score(ns)

main()
