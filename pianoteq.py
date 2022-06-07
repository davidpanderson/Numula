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

# play a MIDI file using pianoteq

import os, platform

if platform.system() == 'Windows':
    prog = "c:/program files/modartt/pianoteq 7/pianoteq 7.exe"
else:
    raise Exception("OS not supported")
    
def play(file):
    cmd = '"%s" --play --midi %s'%(prog, file)
    os.system(cmd)

def midi_to_wav(ifile, ofile, mono=False):
    m = if mono then '--mono' else ''
    cmd = '"%s" %s --wav --headless --midi %s'%(prog, m, file)
    os.system(cmd)
