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

# basic test program: generate notes with everything normally distributed

import random, numpy, math
import numula.nscore as nscore

def normal_time():
    ns = nscore.Score()
    z = []
    min = 0
    for i in range(400):
        x = numpy.random.normal()
        if x > 2: continue
        if x < -2: continue
        z.append(x)
        if x < min: min = x
    for x in z:
        y = math.exp(-(x*x))
        r = int(y*36)
        if r > 0:
            pitch = 60 + random.randrange(-r, r+1)
        else:
            pitch = 60
        time = 15*(x-min)   # 4 min long
        dur = random.randrange(1,6)
        vol = .02 + y*0.9*random.random()
        ns.insert_note(nscore.Note(time, dur, pitch, vol))
    ns.write_midi("data/normal.midi")

normal_time()
