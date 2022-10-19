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

from numula import MidiFile
import random, math

# test program for midiutil.
# play notes from randomly-changing chords

def main():
    f = MidiFile.MIDIFile(1)
    f.addTempo(0, 0, 240)

    c=[0]*4
    time = 0
    dur = 8
    vol = 40
    j = 0
    for i in range(4):
        c[i] = 0
    for i in range(1000):
        #j = random.randrange(4)
        j = (j+1) % 4
        octave = random.randrange(4,8)
        pitch = octave*12 + c[j]
        vol = (math.sin(time/30)+1)*.3 + .1 + 0.15*random.random()
        
        f.addNote(0, 0, pitch, time, dur, int(vol*128))
        #time += random.uniform(.5, 2.)
        time += .5*random.randrange(0,6)
        if i % 30 == 29:
            c[random.randrange(4)] = random.randrange(12)

    with open("data/chords.midi", "wb") as file:
        f.writeFile(file)

main()
