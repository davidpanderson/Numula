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


# play (or render to .WAV) a MIDI file using Pianoteq
# see https://github.com/davidpanderson/Numula/wiki/Pianoteq

import platform, subprocess, os

s = platform.system()
if s == 'Windows':
    prog = "c:/program files/modartt/pianoteq 7/pianoteq 7.exe"
elif s == 'Darwin':
    prog = "/Applications/Pianoteq 7/Pianoteq 7.app/Contents/MacOS/Pianoteq 7"
elif s == 'Linux':
    prog = './Pianoteq 7/amd64/Pianoteq 7'
else:
    raise Exception("OS not supported")
    
def play(file, preset=None):
    if not os.path.isfile(prog):
        raise Exception('Pianoteq missing: %s'%prog)
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s" --play --midi %s%s'%(prog, file, p)
    subprocess.call(cmd, shell=True)

def play_score(ns):
    # TODO: use tempfile
    ns.write_midi('data/temp.midi')
    play('data/temp.midi')

def midi_to_wav(ifile, ofile, mono=False, preset=None):
    if not os.path.isfile(prog):
        raise Exception('Pianoteq missing: %s'%prog)
    m = ' --mono' if mono else ''
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s"%s --wav %s --headless --midi %s%s'%(prog, m, ofile, ifile, p)
    print(cmd)
    subprocess.call(cmd, shell=True)
