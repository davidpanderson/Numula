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

# temporal Shepard tone:
# a melody that always gets faster, but ends up where it started

# N: # of notes
# M: # of repetitions before

from numula.MidiFile import MIDIFile

t = 0
i = 0

def shepard(pitches, nrep, f):
    global t, i
    m = len(pitches)
    nnotes = m*nrep
    k= 0
    for r in range(nrep):
        for j in range(m):
            dt = pow(m, -k/nnotes)
            if i % (m+1) == 0:
                dur = 1
                vol = 1
            else:
                dur = dt
                vol = 1 - k/nnotes
            v = int(vol*127)
            p = pitches[i%m]
            print(i, j, p, dt, vol)
            f.addNote(0, 0, p, t, dur, v)
            t += dt
            i += 1
            k += 1

def main(pitches, nrep, ncycles):
    f = MIDIFile()
    for i in range(ncycles):
        shepard(pitches, nrep, f)
    with open("data/shepard.midi", "wb") as file:
        f.writeFile(file)
        
main([60, 62, 58, 46, 53], 24, 2)
