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

# test program: play random notes

from numula.nscore import *
import random

ns = Score()
for i in range(200):
    pitch = random.randrange(40, 80)
    time = random.uniform(0, 10)
    dur = random.uniform(.1, 1)
    vol = random.uniform(.1, .8)
    ns.insert_note(Note(time, dur, pitch, vol))
print(ns)
ns.write_midi("data/random.midi")
