# This file is part of Numula
# Copyright (C) 2023 David P. Anderson
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

# tests of nuance shorthand functions

from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
from numula.vol_name import *
import numula.pianoteq as pianoteq

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

def test_shift():
    n1 = n('a b c d e f g c')
    n2 = n('a5 b c d e f g c').tag('n2')
    ns = Score([n1,n2])
    s = shift('.1 2/4 .15')
    print(*s, sep='\n')
    ns.time_shift_pft(s, pred = lambda n: 'n2' in n.tags)
    print(ns)
#test_shift()

def test4():
    ns = Score([n('a b c d e f g c')])
    v = tempo('.12p.13 60 10/4 60')
    print(*v, sep='\n')
    ns.tempo_adjust_pft(v, debug=True)
    print(ns)

test4()
