# "wasserklavier" from Six Encores by Luciano Berio
# see https://github.com/davidpanderson/Numula/wiki/Example:-wasserklavier
# Copyright (C) 2022 David P. Anderson

# The score has 6 systems, and each one has several voices.
# We encode each of these separately,
# and give them various tags:
# some of these involve all systems
#   'bass', 'mel'
# and others are specific to a system
#   'inner1', 'inner1a'
#   'sys1'...'sys6'

# nuance structure
# volume
#   there is no overall volume.
#   we do initial volume for each voice separately
#   there is an adjustment for metric accents
# timing
#   1) a global tempo PFT
#   2) functions ta1()...ta6() that do adjustments:
#       - a PFT for pauses
#       - roll() to roll chords
#           almost everything is rolled.
#           We use non-roll as a change of pace

import numpy as np
import numula_path
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq

# Create the score.
# Divide it into the 6 lines of the printed score.
# Put each measure on a new line
#
def make_score():
    top1 = sh_score('3/16 .  d6- 2/8 c 1/8 +c \
        3/8 -f c \
        3/16 . +d- 2/8 c 1/8 +c \
        3/16 [5/8 -f] d- 2/8  c 1/8 +c \
        3/16 -f d- [c -e-] c7 \
    ').tag('mel')
    inner1 = sh_score('6/8 . \
        2/8 a4- 1/8 b- 2/8 c 1/8 d- \
        3/8 e- f \
        g a- \
    ').tag('more').tag('inner1')
    inner1a = sh_score('6/8 . \
        2/8 c4 1/8 d- 2/8 e- 1/8 f \
        3/8 g a- \
        b- c \
        b- \
    ').tag('more').tag('inner1a')
    bass1 = sh_score('6/8 . 3/8 f3 f \
        f f f f f 3/16 f [f5 +d-] \
    ').tag('bass')

    rh2 = sh_score('3/16 [c6 e-] [d- f] d- e- 1/4 c 1/8 c \
        3/16 [-e- +b-] +b- [--f b- +a-] [d- --b-] 1/4 [c 3/8 +g-] 1/8 -c \
        3/16 [--f +c f] +f [b- f -b-] -e- [a- d- f 1/4 a-] --d- 1/8 _ +a- \
        3/16 [c 3/8 d- g-] -b- d- +c [d- -d- 3/8 g-] [e- +e-] \
    ').tag('rh')
    lh2 = sh_score('3/8 [g5- --f] [+f b- ---f] [+f +e-] \
        --g- f e- \
        d- c b- \
        1/4 e- 1/8 f 1/4 [g- ++b-] 1/8 --a- 3/8 [a ++c] \
    ')

    rh3 = sh_score('3/16 [e6- 3/8 f -b- f] [+d- +d-] [e- -f c a- f] +++f 1/4 [--f b-] 1/8 [e- -e-] \
        3/16 [-f b- +g-] [+f +f] 1/8 .  [----c +c  c +c] [-c -c] \
        3/16 . [f +e-] c [+c +c] \
       3/16 [ ---f +f f +f] +f ---c [+g- +g-] \
    ').tag('rh')
    lh3 = sh_score(' 3/8 [b4- -b-] 3/16 [c +a-] [d- -d-] 1/4 [c +g-] 1/8 [-c +c] \
        3/8 [b- f -b-] [a- +a-] \
        3/16 [g- -g-] ++b- 1/4 c 1/8 [c +c] \
        3/16 [---f +f] ++d- 3/8 [--e- -e-] \
    ')

    rh4 = sh_score('3/16 f7 b- [--c a-] [++f +c] \
        [--c -g-]  3/16 [b- +b-  b- +b-] [-e- b- -b-] -e- g- g- \
        [f d-] +d- 1/4 ++d- 1/8 c 3/8 b- \
        1/8 [ ---c e 1/4 a-] [f -a-] 1/4 +g 1/8 [d- +a-] [-e- +d-] \
    ').tag('rh')
    lh4 = sh_score(' 3/16 [d4- -d-] [f5 +d-] d3 a5- \
        [e4- -e-] [e6- d-] 3/8 --d- --c \
        3/16 +c b- 1/4 a- 1/8 [++d- f] 3/16 --g [c ++e] \
        1/4 --f 1/8 [1/4 f 1/8 +d- +b-]  [c -e-] [-f +f] g \
    ')

    rh5 = sh_score('1/32 _ 1/64 e5- +d- 1/6 [e- +d-] 1/12 c 1/4 [b- -d-] +a- \
        [b- +g] 1/6 --d- 1/12 c 1/8 [+g +e- +b-] -d- \
        1/6 [d- +a- d-] 1/12 c 1/4 [b- g -c -e-] [d- +b- +f a-] \
        1/8 [g e- -a- -c] ++d- [--b- +g +d- f +d-] c [b- -e- c -f -a-] ++d- \
    ').tag('rh')
    lh5 = sh_score(' 1/8 [f4 a- +f] [-b- +g] [a- -c -f] [+d- +b-] [c -e- -f] [+f  +d-] \
        [1/4 ---f +f 1/8 ++g +e-] [f -a-] 1/4 [a- --f -f] (less [f +f] \
        [-f +f] [-f +f] [-f +f] \
        [-f +f] [-f +f] [-f +f] less) \
    ')

    rh6 = sh_score('1/8 [(more d7- more) e- +a- d-] c 1/4 [b- g -c a-] [g b- +f a-] \
        [g e- -a- f] [e- g +d- f] [e- c -f -d-] \
        [c e- +b- d-] 1/6 [-d- b-] [+a- c] [-d- b-] \
        1/4 [ (less -f less) c] 3/8 [+b- d- f a-] 1/8 [3/8 --f] \
        1/4 [3/4 a- c] -e- d- \
    ').tag('rh')
    lh6 = sh_score(' 1/4 [f4 g5 b-] [d- -f -f] [f +e- +c] \
        [b- -d- -f] [f +c +a-] [g -b- f] \
        [f a- +g] 1/2 [e -g f] \
        3/4 [ (more g more) 6/4 -c -f] +f \
    ')

    ns = Score()
    ns.append_scores([top1, inner1, inner1a, bass1], 'line1')
    ns.append_scores([rh2, lh2], 'line2')
    ns.append_scores([rh3, lh3], 'line3')
    ns.append_scores([rh4, lh4], 'line4')
    ns.append_scores([rh5, lh5], 'line5')
    ns.append_scores([rh6, lh6], 'line6')

    # add measures (for metric accents)
    #
    for i in range(5):
        ns.append_measure(6/8, '6/8')
    for i in range(5):
        ns.append_measure(9/8, '9/8')
    for i in range(4):
        ns.append_measure(6/8, '6/8')
    for i in range(2):
        ns.append_measure(9/8, '9/8')
    for i in range(10):
        ns.append_measure(3/4, '3/4')
    return ns

#  volume

def set_vol(ns):
    ns.vol_adjust_pft(
        sh_vol('mm 30/8 mm \
            [ pp 9/8 [ ppp 18/8 [ pp 9/8 p \
            p 27/8 mp \
            [ p 17/8 ppp 15/8 pp \
            pp 24/8 f \
            f 24/8 ppp \
            ppp 6/8 ppp \
        ')
    )

    # system 1
    ns.vol_adjust_pft(
        sh_vol('pp 12/8 p 9/8 mf ] pp 6/8 ppp ] p 3/8 p'),
        selector = lambda n: 'mel' in n.tags
    )
    ns.vol_adjust_pft(
        sh_vol('mm 6/8 mm [ ppp 12/8 p 12/8 ppp'),
        selector = lambda n: 'inner1' in n.tags
    )
    ns.vol_adjust_pft(
        sh_vol('mm 6/8 mm [ ppp 12/8 pp 12/8 ppp'),
        selector = lambda n: 'inner1a' in n.tags
    )
    ns.vol_adjust_pft(
        sh_vol('mm 6/8 mm [ ppp 12/8 p 12/8 ppp'),
        selector = lambda n: 'bass' in n.tags
    )

    # voice to top/bottom
    #ns.vol_adjust(.2, lambda n: 'top' in n.tags and 'rh' in n.tags, VOL_ADD)
    #ns.vol_adjust(.6, lambda n: 'top' not in n.tags and 'bottom' not in n.tags)
    #ns.vol_adjust(.8, lambda n: 'top' not in n.tags and 'bottom' in n.tags)

    # metric accents
    ns.vol_adjust(1.1, lambda n: n.measure_offset==0)
    ns.vol_adjust(0.9, lambda n: n.measure_type=='9/8' and n.measure_offset not in [0, 3/8, 6/8])
    ns.vol_adjust(0.9, lambda n: n.measure_type=='6/8' and n.measure_offset not in [0, 3/8])
    ns.vol_adjust(0.9, lambda n: n.measure_type=='3/4' and n.measure_offset not in [0, 1/4, 2/4])

    # bring out inner voices
    #ns.vol_adjust(.1, lambda n: 'more' in n.tags, mode=VOL_ADD)
    #ns.vol_adjust(.7, lambda n: 'less' in n.tags)

#  timing

def set_tempo(ns):
    ns.tempo_adjust_pft(
        sh_tempo('\
            50 6/8 50 60 9/8 60 70 6/8 70 55 9/8 40 \
            65 30/8 60 \
            65 9/8 55 60 9/8 70 18/8 80 \
            65 27/8 55 \
            55 24/8 50 |time_change 30 6/8 40 \
            40 24/8 50 \
            50 30/8 30 \
        ')
    )

# pauses/rolls -  do this after overall tempo

# start times of the 6 systems
t1 = 0
t2 = t1 + 30/8
t3 = t2 + 36/8
t4 = t3 + 27/8
t5 = t4 + 30/8
t6 = t5 + 24/8
tend = t6 + 30/8

roll4_long = roller(4, -.3, .2, .8, .05)
roll4 = roller(4, -.1, .1, .8)
roll5 = roller(5, -.15, .1, .8)
roll5_long = roller(5, -.3, .2, .8)
roll6 = roller(6, -.2, .1, .8)
roll7 = roller(7, -.2, .15, .8)
roll3 = roller(3, -.1, .1, .8)
roll2 = [-.1, .1]
roll_grace4 = [-.12, -.09, 0, .08]

def ta1(ns):
    ns.tempo_adjust_pft(
        sh_tempo('5/8 . .2p 1/8 . \
            6/8 . \
            p.3 6/8 . \
            5/8 . .3p 1/8 . \
            9/16 . .3p \
        ')
    )
    m = 6/8
    ns.roll(m, roll4_long)
    ns.roll(m+2/8, roll2)
    ns.roll(m+3/8, roll4)
    ns.roll(m+5/8, roll2)
    m += 6/8
    ns.roll(m, roll3)
    ns.roll(m+3/8, roll4)
    m += 6/8
    ns.roll(m, roll4)
    ns.roll(m+3/8, roll4)
    m += 6/8
    ns.roll(m, roll3)
    ns.roll(m+3/8, roll3)

def ta2(ns):
    ns.tempo_adjust_pft(
        sh_tempo('6/8 . p.15 27/8 . p.1'),
        t2
    )
    m = t2 + 9/8
    ns.roll(m+3/8, roll4)
    ns.roll(m+6/8, roll3)
    m += 9/8
    ns.roll(m, roll4)
    ns.roll(m+3/8, roll4)
    ns.roll(m+6/8, roll5)
    m += 9/8
    ns.roll(m, roll4)
    ns.roll(m+3/8, roll3)
    ns.roll(m+6/8, roll5_long)


def ta3(ns):
    ns.tempo_adjust_pft(
        sh_tempo('6/8 . p.15 3/16 . p.15'),
        t3
    )
    m = t3
    ns.roll(m+3/8, roll7)
    m += 9/8
    ns.roll(m+5/8, roll_grace4)
    m += 6/8
    m += 6/8
    ns.roll(m, roll_grace4, selector=lambda n: 'rh' in n.tags)

def ta4(ns):
    ns.tempo_adjust_pft(
        sh_tempo('9/8 . p.1 6/8 . p.2'),
        t4
    )
    m = t4
    m += 6/8
    ns.roll(m+3/16, roll_grace4, selector=lambda n: 'rh' in n.tags)
    ns.roll(m+3/8, roll3, selector=lambda n: 'rh' in n.tags)

def ta5(ns):
    m = t + 6/8
    ns.roll(m, roll_grace4, selector=lambda n: 'rh' in n.tags)
    m += 6/8
    ns.roll(m,  roll6)
    m += 6/8
    ns.roll(m+2/8, np.linspace(-.2, .1, 4), selector=lambda n: 'rh' in n.tags)
    ns.roll(m+4/8, np.linspace(-.2, .1, 4), selector=lambda n: 'rh' in n.tags)
    m += 6/8
    ns.roll(m, roll4, selector=lambda n: 'rh' in n.tags)
    ns.roll(m+2/8, roll5, selector=lambda n: 'rh' in n.tags)
    ns.roll(m+4/8, roll5, selector=lambda n: 'rh' in n.tags)

def ta6(ns):
    ns.tempo_adjust_pft(
        sh_tempo('14/4 . p10'),
        t6
    )
    m = t6
    ns.roll(m, roll7)
    ns.roll(m+2/8, roll7)
    ns.roll(m+4/8, roll7)
    m += 6/8
    ns.roll(m, roll7)
    ns.roll(m+2/8, roll7)
    ns.roll(m+4/8, roll7)
    m += 6/8
    ns.roll(m, roll7)
    ns.roll(t6+14/8, roller(3, -.4, .1), selector=lambda n: 'lh' in n.tags)
    m += 6/8
    ns.roll(m, [-.4, -.3, .2, -.1, -.2])

def time_adjust(ns):
    ta1(ns)
    ta2(ns)
    ta3(ns)
    ta4(ns)
    ta5(ns)
    ta6(ns)
    #ns.t_random_normal(.015, 2)
    
def main():
    ns = make_score()
    #ns.verbose = True
    if True:
        set_vol(ns)
        set_tempo(ns)
        time_adjust(ns)
        #print(ns)

    if True:
        numula.pianoteq.play_score(ns,
            #preset='My Presets/NY Steinway D Classical (for wasser)'
            preset='NY Steinway D Classical'
            #score_time = 30/8
        )
    else:
        ns.write_midi('data/wasserklavier.midi')
        numula.pianoteq.midi_to_wav(
            'data/wasserklavier.midi',
            'data/wasserklavier9.wav',
            version=9,
            preset='NY Steinway D Classical'
        )

main()
