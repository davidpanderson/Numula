# This file is part of Numula
# Copyright (C) 2022 David P. Anderson
#
# Numula is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Numula is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Numula.  If not, see <http://www.gnu.org/licenses/>.


# "wasserklavier" from Six Encores by Luciano Berio
# see https://github.com/davidpanderson/Numula/wiki/Example:-wasserklavier

import numpy as np
from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq

# create the score (notes and measures)
#
def make_score():
    rh1 = n('3/16 .  ++d- 2/8 c 1/8 +c \
        3/8 -f [c (more -c more) ] \
        3/16 [ -g 3/8 (more +e- more) ] +d- 2/8 [c (more -f more) ] 1/8 ++c \
        3/16 [5/8 -f 3/8 (more -g more) ] +d- 2/8  [c (more a- more) ] 1/8 ++c \
        3/16 -f d- [c -e-] ++c \
    ').tag('rh')
    rh2 = n('3/16 [+c e-] [d- f] d- e- 1/4 c 1/8 c \
        3/16 [-e- +b-] +b- [--f b- +a-] [d- --b-] 1/4 [c 3/8 +g-] 1/8 -c \
        3/16 [--f +c f] +f [b- f -b-] -e- [a- d- f 1/4 a-] --d- 1/8 _ +a- \
        3/16 [c 3/8 d- g-] -b- d- +c [d- -d- 3/8 g-] [e- +e-] \
    ').tag('rh')
    rh3 = n('3/16 [++e- 3/8 f -b- f] [+d- +d-] [e- -f c a- f] +++f 1/4 [--f b-] 1/8 [e- -e-] \
        3/16 [-f b- +g-] [+f +f] 1/8 .  [----c +c  c +c] [-c -c] \
        3/16 . [f +e-] c [+c +c] \
       3/16 [ ---f +f f +f] +f ---c [+g- +g-] \
    ').tag('rh')
    rh4 = n('3/16 +++f b- [--c a-] [++f +c] \
        [--c -g-]  3/16 [b- +b-  b- +b-] [-e- b- -b-] -e- g- g- \
        [f d-] +d- 1/4 ++d- 1/8 c 3/8 b- \
        1/8 [ ---c e 1/4 a-] [f -a-] 1/4 +g 1/8 [d- +a-] [-e- +d-] \
    ').tag('rh')
    rh5 = n('1/32 _ 1/64 e- +d- 1/6 [e- +d-] 1/12 c 1/4 [b- -d-] +a- \
        [b- +g] 1/6 --d- 1/12 c 1/8 [+g +e- +b-] -d- \
        1/6 [d- +a- d-] 1/12 c 1/4 [b- g -c -e-] [d- +b- +f a-] \
        1/8 [g e- -a- -c] ++d- [--b- +g +d- f +d-] c [b- -e- c -f -a-] ++d- \
    ').tag('rh')
    rh6 = n('1/8 [(more +++d- more) e- +a- d-] c 1/4 [b- g -c a-] [g b- +f a-] \
        [g e- -a- f] [e- g +d- f] [e- c -f -d-] \
        [c e- +b- d-] 1/6 [-d- b-] [+a- c] [-d- b-] \
        1/4 [ (less -f less) c] 3/8 [+b- d- f a-] 1/8 [3/8 --f] \
        1/4 [3/4 a- c] -e- d- \
    ').tag('rh')
    lh1 = n('6/8 . 2/8 [--f +c (more +a- more) ] 1/8 [-d- (more +b- more) ] 2/8 [--f +e-] 1/8 [f (more +d- more) ] \
        3/8 --f [f ++a-] \
        [--f ++b-] [--f ++c] \
        [--f ++b-] 3/16 --f [++f +d-] \
    ')
    lh2 = n('3/8 [+g- --f] [+f b- ---f] [+f +e-] \
        --g- f e- \
        d- c b- \
        1/4 e- 1/8 f 1/4 [g- ++b-] 1/8 --a- 3/8 [a ++c] \
    ')
    lh3 = n(' 3/8 [b- -b-] 3/16 [c +a-] [d- -d-] 1/4 [c +g-] 1/8 [-c +c] \
        3/8 [b- f -b-] [a- +a-] \
        3/16 [g- -g-] ++b- 1/4 c 1/8 [c +c] \
        3/16 [---f +f] ++d- 3/8 [--e- -e-] \
    ')
    lh4 = n(' 3/16 [-d- -d-] [+++f +d-] ---d +++a- \
        [--e- -e-] [+++e- d-] 3/8 --d- --c \
        3/16 +c b- 1/4 a- 1/8 [++d- f] 3/16 --g [c ++e] \
        1/4 --f 1/8 [1/4 f 1/8 +d- +b-]  [c -e-] [-f +f] g \
    ')
    lh5 = n(' 1/8 [-f a- +f] [-b- +g] [a- -c -f] [+d- +b-] [c -e- -f] [+f  +d-] \
        [1/4 ---f +f 1/8 ++g +e-] [f -a-] 1/4 [a- --f -f] (less [f +f] \
        [-f +f] [-f +f] [-f +f] \
        [-f +f] [-f +f] [-f +f] less) \
    ')
    lh6 = n(' 1/4 [-f ++g b-] [d- -f -f] [f +e- +c] \
        [b- -d- -f] [f +c +a-] [g -b- f] \
        [f a- +g] 1/2 [e -g f] \
        3/4 [ (more g more) 6/4 -c -f] +f \
    ')
    ns = Score()
    ns.append_score([rh1, lh1], 'line1')
    ns.append_score([rh2, lh2], 'line2')
    ns.append_score([rh3, lh3], 'line3')
    ns.append_score([rh4, lh4], 'line4')
    ns.append_score([rh5, lh5], 'line5')
    ns.append_score([rh6, lh6], 'line6')
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
        vol('ppp 30/8 pp \
            pp 9/8 ppp 18/8 pp 9/8 p \
            p 27/8 mp \
            [ p 17/8 ppp 15/8 pp \
            pp 24/8 f \
            f 24/8 ppp \
            ppp 6/8 ppp \
        ')
    )

    # bring out inner voices
    ns.vol_adjust(2.5, lambda n: 'more' in n.tags)
    ns.vol_adjust(.7, lambda n: 'less' in n.tags)
    
    # voice to top/bottom
    ns.vol_adjust(1.1, lambda n: 'top' in n.tags and 'rh' in n.tags)
    ns.vol_adjust(.6, lambda n: 'top' not in n.tags and 'bottom' not in n.tags)
    ns.vol_adjust(.8, lambda n: 'top' not in n.tags and 'bottom' in n.tags)

    # metric accents
    #ns.vol_adjust(1.1, lambda n: n.measure_offset==0)
    ns.vol_adjust(0.9, lambda n: n.measure_type=='9/8' and n.measure_offset not in [0, 3/8, 6/8])
    ns.vol_adjust(0.9, lambda n: n.measure_type=='6/8' and n.measure_offset not in [0, 3/8])
    ns.vol_adjust(0.9, lambda n: n.measure_type=='3/4' and n.measure_offset not in [0, 1, 2])

#  timing

def set_tempo(ns):
    ns.tempo_adjust_pft(
        tempo('65 30/8 60 \
            65 9/8 55 60 9/8 70 18/8 80 \
            65 27/8 55 \
            55 24/8 50 |time_change 30 6/8 40 \
            40 24/8 50 \
            50 30/8 30 \
        ')
    )

# timing adjustment -  do this after overall tempo

# durations of the 6 lines:
t1 = 30/8
t2 = 36/8
t3 = 27/8
t4 = 30/8
t5 = 24/8
t6 = 30/8

def ta1(ns):
    t = 0
    ns.t_adjust_notes(-.2, lambda n: 'line1' in n.tags and n.pitch==41)
    ns.roll(t+6/8,  np.linspace(-.1, 0, 4))
    ns.pause_after(t+12/8, .2)
    ns.pause_after(t+30/8, .15)
def ta2(ns):
    t = t1
    ns.pause_after(t+6/8, .15)
    ns.pause_after(t+33/8, .1)
def ta3(ns):
    t = t1 + t2
    ns.roll(t+3/8,  np.linspace(-.3, .1, 7))
    ns.pause_after(t+6/8, .15)
    ns.roll(t+13/8, np.linspace(-.12, .1, 4))
    ns.pause_after(t+6/8+3/16, .15)
    ns.roll(t+21/8, np.linspace(-.12, .1, 4), pred=lambda n: 'rh' in n.tags)
def ta4(ns):
    t = t1 + t2 + t3
    ns.roll(t+6/8+3/16, np.linspace(-.12, .1, 4), pred=lambda n: 'rh' in n.tags)
    ns.roll(t+6/8+3/8,  np.linspace(-.2, .1, 3), pred=lambda n: 'rh' in n.tags)
    ns.pause_after(t+6/8+3/8, .1)
    ns.pause_after(t+15/8, .2)
def ta5(ns):
    t = t1 + t2 + t3 + t4
    ns.roll(t+6/8,  np.linspace(-.4, .1, 6))
    ns.roll(t+14/8, np.linspace(-.2, .1, 4), pred=lambda n: 'rh' in n.tags)
    ns.roll(t+16/8, np.linspace(-.2, .1, 4), pred=lambda n: 'rh' in n.tags)
    ns.roll(t+18/8, np.linspace(-.2, .1, 4), pred=lambda n: 'rh' in n.tags)
    ns.roll(t+20/8, np.linspace(-.2, .1, 5), pred=lambda n: 'rh' in n.tags)
    ns.roll(t+22/8, np.linspace(-.2, .1, 5), pred=lambda n: 'rh' in n.tags)
def ta6(ns):
    t = t1 + t2 + t3 + t4 + t5
    ns.roll(t,  np.linspace(-.3, .1, 3), pred=lambda n: 'rh' not in n.tags)
    ns.roll(t+2/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+4/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+6/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+8/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+10/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+12/8,  np.linspace(-.4, .1, 7))
    ns.roll(t+14/8,  np.linspace(-.4, .1, 3), pred=lambda n: 'rh' not in n.tags)
    ns.roll(t+18/8,  [-.4, -.3, .2, -.1, -.2])
    ns.pause_after(t+14/4, 10)

def time_adjust(ns):
    ta1(ns)
    ta2(ns)
    ta3(ns)
    ta4(ns)
    ta5(ns)
    ta6(ns)
    ns.t_random_normal(.015, 2)
    
def main():
    ns = make_score()
    if True:
        set_vol(ns)
        set_tempo(ns)
        time_adjust(ns)
        print(ns)
        ns.write_midi('data/wasserklavier.midi')
        numula.pianoteq.play('data/wasserklavier.midi',
            preset='My Presets/NY Steinway D Classical (for wasser)'
        )
    else:
        ns.write_midi('data/wasserklavier_plain.midi')

main()
