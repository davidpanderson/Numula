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

# tests of nuance functions (not shorthands)

import numula_path
from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq as pianoteq

# various timing-related functions
def test1(mode, name, pause):
    print('mode:', name, 'pause:', pause);
    ns = sh_score('c d e [f a c] g a b c d e f')
    ns.tempo = 120
    s1 = sh_tempo('60 8/4 120')
    if pause:
        s2 = sh_tempo('60 4/4 90 .1p 4/4 120')
        s3 = sh_tempo('1 4/4 .75 .1p 4/4 .5', bpm=False)
    else:
        s2 = sh_tempo('60 4/4 90 4/4 120')
        s3 = sh_tempo('1 8/4 .5', bpm=False)

    if mode == TIME_SLOWNESS:
        ns.tempo_adjust_pft(s3, mode=mode, normalize=False)
    else:
        ns.tempo_adjust_pft(s2, mode=mode, normalize=False, debug=False)
    #ns.pause_before(3/4, .7, False)
    #ns.roll(3/4, [-.2, -.1, 0], True)
    print(ns)
    #pianoteq.play_score(ns)
#test1(TIME_TEMPO, 'tempo', False)
#test1(TIME_TEMPO, 'tempo', True)
#test1(TIME_PSEUDO_TEMPO, 'pseudo-tempo', False)
#test1(TIME_PSEUDO_TEMPO, 'pseudo-tempo', True)
#test1(TIME_SLOWNESS, 'slowness', False)
#test1(TIME_SLOWNESS, 'slowness', True)

def test2():
    ns = Score()
    ns.insert_score(sh_score('c d e (foo [f a c] g foo) a b c'))
    ns.insert_measure(Measure(0, 4/4, '4/4'))
    ns.insert_measure(Measure(1, 4/4, '4/4'))
    ns.start_adjust_list([.1, .2], lambda x: 'foo' in x.tags)
    ns.t_random_uniform(-.1, .1)
    ns.t_random_normal(.1, 3)
    ns.v_random_normal(.1)
    ns.v_random_uniform(.9, 1.1)
    print(ns)
    pianoteq.play_score(ns)
#test2()

def test4():
    ns = sh_score('c d e f g')
    ns.vol_adjust_pft([
        Linear(pp, ff, 1/8),
        Linear(ff, p, 2/4)
    ])
    print(ns)
#test4()
    
def test_dur_pft():
    ns = Score()
    for i in range(8):
        ns.append_score(sh_score('1/8 c d e f g a b c'))
    ns.perf_dur_pft(
        [
            Linear(.1, 1.5, 8/4),
            Linear(1.5, .1, 8/4)
        ], 0, rel=True
    )
    ns.perf_dur_pft(
        [
            Linear(.1, .4, 8/4),
            Linear(.4, .1, 8/4)
        ], 16/4, rel=False
    )
    print(ns)
    ns.write_midi('data/test_dur_pft.midi')
    pianoteq.play_score(ns)
#test_dur_pft()

def test_pft_value():
    p = [
            Linear(0, 1, 1, closed_end=False),
            Linear(3, 4, 1)
        ]
    v = PFTValue(p)
    for i in range(25):
        x = i/10
        print(x, v.value(x))
#test_pft_value()

# use a PFT to emphasize particular beats
def test_vol():
    ns = Score()
    for i in range(2):
        ns.append_score(sh_score('1/8 c d e f g a b c'))
    ns.vol_adjust_pft(
        [
            Unity(2/4),
            Accent(1.3),
            Unity(1/4),
            Accent(1.5)
        ], 0
    )
    print(ns)
    pianoteq.play_score(ns)
#test_vol()

def test_pbl():
    ns = sh_score('c d e [f a c] g a b c')
    ns.pause_before_list([3/4, 5/4, 13/8], [.1, .2, .3])
    print(ns)
#test_pbl()

def scale():
    ns = Score()
    ns.append_scores(
        [
            sh_score('c5 d e f c d e f c d e f').tag('rh'),
            sh_score('c4 d e f c d e f c d e f').tag('lh')
        ]
    )

    ns.vol_adjust_pft(
        [
            Linear(pp, ff, 4/4),
            Linear(f, p, 4/4, closed_start=True)
        ], selector=lambda n: 'rh' in n.tags
    )

    print(ns)
    print('---')
    x = sh_tempo('80 6/4 40 2/4 60')
    print(*x, sep='\n')
    pft_normalize_dur(x, 4/4)
    print('---')
    print(*x, sep='\n')
    ns.tempo_adjust_pft(
        x,
        4/4,
        lambda n: 'rh' in n.tags,
        True
    )

    print(ns)
    #pianoteq.play_score(ns)
#scale()

# various rolled chords
def test_roll():
    ns = sh_score('2/4 *4 [c4 +g c e g c +c e] *')
    ns.roll(0, roller(8, 0, .7))
    ns.roll(2/4, roller(8, 0, .7, .7))
    ns.roll(4/4, roller(8, 0, .7, 1.3))
    ns.roll(6/4, roller(8, 0, .7, .8, .2, .2))
    pianoteq.play_score(ns)
#test_roll()

def test_orn():
    sop = sh_score('1/4 c 3/8 orn[210(12)1 f+ g a rep=6 3/8] 1/16 f+ g \
').tag('soprano')
    alto = sh_score('1/4 c c c').tag('alto')
    ns = Score(tempo=55)
    ns.append_scores([sop, alto])
    x = sh_tempo('40 1/2 80 1/4 40')
    pft_normalize_dur(x, 2/4)
    ns.tempo_adjust_pft(x, 1/4, lambda n: 'soprano' in n.tags, normalize=True, debug=True)
    print('second')
    print(ns)
    ns.perf_dur_rel(0.9,
        lambda n: 'soprano' in n.tags and 'slur' not in n.tags and 'orn' not in n.tags
    )

    print('third')
    print(ns)

test_orn()

