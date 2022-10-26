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


# convert a MIDI file to a Score
# see https://github.com/davidpanderson/Numula/wiki/read_midifile.py

import mido, copy
import numula.nscore as nscore

def print_midi_event(e):
    if e.type == 'note_on':
        print('note_on pitch %s vel %d time %d'%(note.pitch_name(e.note), e.velocity, e.time))
    elif e.type == 'note_off':
        print('note_off pitch %s time %d'%(note.pitch_name(e.note), e.time))
    else:
        print(e)
        
def read_midifile(file, ticks_per_beat=960, use_velocity=True):
    debug = False
    ticks_per_measure = ticks_per_beat*4
    mf = mido.MidiFile(file)
    ns = nscore.Score()
    for i, track in enumerate(mf.tracks):
        if debug:
            print('track', i)
        t = 0
        tag = 'track%d'%i
        notes = [None]*128
        for msg in track:
            if debug:
                print_midi_event(msg)
            if msg.type == 'note_on':
                t += msg.time/ticks_per_measure
                if use_velocity:
                    vol = msg.velocity/128
                else:
                    vol = .5
                pitch = msg.note
                if notes[pitch]:
                    # overlap case.  End current note at this pitch, and start a new one
                    n = notes[pitch]
                    n.dur = t-n.time
                    if debug:
                        print('inserting note, overlap case')
                        n.print()
                    ns.insert_note(copy.deepcopy(n))
                    n.time = t
                    n.vol = vol
                else:
                    n = nscore.Note(t, 0, pitch, vol, [tag])
                    notes[pitch] = n
            elif msg.type == 'note_off':
                t += msg.time/3840
                pitch = msg.note
                if not notes[pitch]:
                    # this happens in overlap case
                    continue
                n = notes[pitch]
                notes[pitch] = None
                n.dur = t-n.time
                ns.insert_note(n)
                if debug:
                    print('inserting note, regular case')
                    n.print()
    return ns
    
def print_midifile(file):
    mid = mido.MidiFile(file)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
