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

from notate import *
from nscore import *
from nuance import *
from nuance_notate import *

# various timing-related functions
def test1():
    ns = Score()
    ns.insert_score(0, n('c d e [f a c] g a b c'))
    ns.done()
    ns.tempo_adjust_pft([linear(60, 120, 8/4)])
    ns.pause_before(3/4, .7)
    ns.roll(3/4, [-.2, -.1, 0], True, True)
    print(ns)
    ns.write_midi('data/test1.midi')
#test1()

def test2():
    ns = Score()
    ns.insert_score(n('c d e (foo [f a c] g foo) a b c'), 0)
    ns.insert_measure(Measure(0, 4/4, '4/4'))
    ns.insert_measure(Measure(1, 4/4, '4/4'))
    ns.done()
    ns.t_adjust_list([.1, .2], lambda x: 'foo' in x.tags)
    ns.t_random_uniform(-.1, .1)
    ns.t_random_normal(.1, 3)
    print(ns)
    ns.write_midi('data/test2.midi')
#test2()

def test3():
    ns = Score([n('c d e f g')])
    ns.done()
    ns.tempo_adjust_pft([
        linear(60, 60, 2/4),
        delta(.1, False),
        linear(30, 30, 2/4)
    ])
    print(ns)
#test3()

def test4():
    ns = Score([n('c d e f g')])
    ns.done()
    ns.vol_adjust_pft([
        linear(pp, ff, 1/8),
        linear(ff, p, 2/4)
    ])
    print(ns)
#test4()
    
def test_dur_pft():
    ns = Score()
    for i in range(8):
        ns.append_score([n('1/8 c d e f g a b c')])
    ns.done()
    ns.perf_dur_pft(
        [
            linear(.1, 1.5, 8/4),
            linear(1.5, .1, 8/4)
        ], 0, rel=True
    )
    ns.perf_dur_pft(
        [
            linear(.1, .4, 8/4),
            linear(.4, .1, 8/4)
        ], 16/4, rel=False
    )
    print(ns)
    ns.write_midi('data/test_dur_pft.midi')

def test_pft_value():
    p = [
            linear(0, 1, 1, closed_end=False),
            linear(3, 4, 1)
        ]
    v = pft_value(p)
    for i in range(25):
        x = i/10
        print(x, v.value(x))
#test_pft_value()

# use a PFT to emphasize particular beats
def test_vol():
    ns = Score()
    for i in range(2):
        ns.append_score([n('1/8 c d e f g a b c')])
    ns.done()
    ns.vol_adjust_pft(
        [
            unity(2/4),
            accent(1.3),
            unity(1/4),
            accent(1.5)
        ], 0
    )
    print(ns)

#test_vol()

def test_ped():
    ns = Score()
    for i in range(2):
        ns.append_score([n('1/8 c d e f g a b c')])
    #ns.insert_pedal(PedalUse(1/4, 3/4))
    #ns.pedal_pft([PedalSeg(3/16, 0), PedalSeg(2/4, 1)])
    ns.pedal_pft(pedal('- 1/4 + 1/8 + 1/4 - 4/4'))
    ns.done()
    print(ns)

test_ped()
