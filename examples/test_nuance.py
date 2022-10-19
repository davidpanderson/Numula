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

from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq as pianoteq

# various timing-related functions
def test1():
    ns = n('c d e [f a c] g a b c')
    #ns.tempo_adjust_pft([Linear(60, 120, 8/4)])
    ns.pause_before(3/4, .7, False)
    #ns.roll(3/4, [-.2, -.1, 0], True, True)
    print(ns)
    pianoteq.play_score(ns)
#test1()

def test2():
    ns = Score()
    ns.insert_score(n('c d e (foo [f a c] g foo) a b c'))
    ns.insert_measure(Measure(0, 4/4, '4/4'))
    ns.insert_measure(Measure(1, 4/4, '4/4'))
    ns.t_adjust_list([.1, .2], lambda x: 'foo' in x.tags)
    ns.t_random_uniform(-.1, .1)
    ns.t_random_normal(.1, 3)
    print(ns)
    pianoteq.play_score(ns)
#test2()

def test3():
    ns = Score([n('a b c d e f g c')], tempo=120)
    x = [
        Delta(.05, False),
        Linear(60, 60, 2/4),
        Delta(.1, False),
        Delta(.2, True),
        Linear(60, 60, 2/4)
    ]
    x = tempo('60 2/4 60 .1p.2 60 2/4 60')
    #x = tempo('60 2/4 60')
    print(*x, sep='\n')
    ns.tempo_adjust_pft(x)
    print(ns)
    pianoteq.play_score(ns)
#test3()

def test4():
    ns = Score([n('c d e f g')])
    ns.vol_adjust_pft([
        Linear(pp, ff, 1/8),
        Linear(ff, p, 2/4)
    ])
    print(ns)
#test4()
    
def test_dur_pft():
    ns = Score()
    for i in range(8):
        ns.append_score([n('1/8 c d e f g a b c')])
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
    v = PftValue(p)
    for i in range(25):
        x = i/10
        print(x, v.value(x))
#test_pft_value()

# use a PFT to emphasize particular beats
def test_vol():
    ns = Score()
    for i in range(2):
        ns.append_score([n('1/8 c d e f g a b c')])
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

def test_ped():
    ns = Score()
    for i in range(2):
        ns.append_score([n('1/8 c d e f g a b c')])
    #ns.insert_pedal(PedalUse(1/4, 3/4))
    #ns.pedal_pft([PedalSeg(3/16, 0), PedalSeg(2/4, 1)])
    ns.pedal_pft(pedal('- 1/4 + 1/8 + 1/4 - 4/4'))
    print(ns)
    pianoteq.play_score(ns)
#test_ped()

def test_pbl():
    ns = Score([n('c d e [f a c] g a b c')], verbose=True)
    ns.pause_before_list([3/4, 5/4, 13/8], [.1, .2, .3])
    print(ns)
test_pbl()

def test_tag():
    ns = Score([
        n(' |300 1/16 [c f a- c] g a- b- c d e f'),
        n(' |300 1/4 f3 1/8 . [c f a- c] *4 [-c e g b- c] * ')
    ], verbose=True)
    print(ns)
#test_tag()
        
