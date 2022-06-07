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

from MidiFile import MIDIFile

def chromatic():
    track = 0
    channel = 0
    time = 0
    dur = 0.5
    tempo = 120
    vol = 80

    f = MIDIFile(deinterleave=False)
    f.addTempo(track, time, tempo)
    
    for pitch in range (50,70):
        f.addNote(track, channel, pitch, time, dur, vol)
        time += 1

    f.addControllerEvent(track, channel, 5, 64, 70)
    f.addControllerEvent(track, channel, 15, 64, 0)
    
    with open("data/chromatic.midi", "wb") as file:
        f.writeFile(file)

def vol_sweep():
    f = MIDIFile(deinterleave=False)
    t = 0
    for v in range(0, 128, 8):
        f.addNote(0, 0, 60, t, 1, v)
        t += 1
    with open("data/vol_sweep.midi", "wb") as file:
        f.writeFile(file)

vol_sweep()
        
#chromatic()
                         
# show a bug in MIDIFile: crashes if 2 notes w/ same time and pitch
#
def mf_bug():
    f = MIDIFile()
    f.addTempo(0, 0, 120)
    f.addNote(0, 0, 60, 0, .5, 64);
    f.addNote(0, 0, 60, 0, .4, 64);
    with open("data/test.midi", "wb") as file:
        f.writeFile(file)

#mf_bug()
