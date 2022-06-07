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

from midiutil import MIDIFile
import colorednoise as cn

# 1/f noise
# see https://github.com/felixpatzelt/colorednoise

def cn_test():
    beta = 1
    samples = 100
    y = cn.powerlaw_psd_gaussian(beta, samples)
    f = MIDIFile(1)
    f.addTempo(0, 0, 120)
    pitch = 48
    dur = 1
    vol = 60
    time = 0
    for i in range(samples):
        pitch = 60+12*y[i]
        f.addNote(0, 0, int(pitch), time, dur, vol)
        print(pitch, y[i])
        time += 1
    with open("data/colored_noise.midi", "wb") as file:
        f.writeFile(file)
        
cn_test()
