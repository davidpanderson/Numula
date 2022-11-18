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

# return path of latest PianoTeq executable
#
def pianoteq_path():
    s = platform.system()
    for v in (8, 7):
        if s == 'Windows':
            p = 'c:/program files/modartt/pianoteq %d/pianoteq %d.exe'%(v,v)
        elif s == 'Darwin':
            p = '/Applications/Pianoteq %d/Pianoteq %d.app/Contents/MacOS/Pianoteq %d'%(v,v,v)
        elif s == 'Linux':
            p = './Pianoteq %d/amd64/Pianoteq %d'%(v,v)
        else:
            raise Exception("OS not supported")
        if os.path.isfile(p):
            return p
    raise Exception('Pianoteq not found')
    
def play(file, preset=None):
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s" --play --midi %s%s'%(pianoteq_path(), file, p)
    subprocess.call(cmd, shell=True)

def play_score(ns):
    # TODO: use tempfile
    ns.write_midi('data/temp.midi')
    play('data/temp.midi')

def midi_to_wav(ifile, ofile, mono=False, preset=None):
    m = ' --mono' if mono else ''
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s"%s --wav %s --headless --midi %s%s'%(pianoteq_path(), m, ofile, ifile, p)
    print(cmd)
    subprocess.call(cmd, shell=True)
