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

# tests of score notation (n())

from numula.nscore import *
from numula.notate_score import *

def test1():
    s = 'c (foo d 1/8 _ e foo)'
    ns = ScoreBasic()
    ns.append_score([n(s)])
    print(ns)
    ns.write_midi('data/test1.midi')

#test1()

def test2():
    s = n('<1/2 1/4> a b c d e f')
    print(s)

#test2()

def test3():
    foo = iter([1,2,3])
    s = n('<x> a b c <1/4 1/2> d e f g', x=foo)
    print(s)

#test3()

def test4():
    s = n('<1/4 1/2> [c 1/1 d] e')
    print(s)

#test4()

def test_tag():
    ns = ScoreBasic([
        n(' |300 1/16 [c f a- c] g a- b- c d e f'),
        n(' |300 1/4 f3 1/8 . [c f a- c] *4 [-c e g b- c] * ')
    ], verbose=True)
    print(ns)
test_tag()
