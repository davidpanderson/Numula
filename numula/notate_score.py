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

# textual music notation
# E.g. n('1/8 a b c') returns a list of Note objects for 8th note A, B, C
# see https://github.com/davidpanderson/Numula/wiki/notate.py

import numula.nscore as nscore
from numula.notate import *

note_names = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
pitch_offset = [0, 2, 4, 5, 7, 9, 11]

# Parse a string of the form ++b- or b5-.
# Return a pitch.
#
def parse_pitch(items, i, cur_pitch):
    got_pitch = False
    off = [0,0]
    s = items[i]
    absolute = False
    for c in s:
        if c in note_names:
            if got_pitch:
                show_context(items, i)
                raise Exception('already have pitch in %s'%s)
            pitch_class = pitch_offset[note_names.index(c)]
            got_pitch = True
        elif c == '+':
            i = 1 if got_pitch else 0
            if off[i] < 0:
                show_context(items, i)
                raise Exception('bad offset')
            off[i] += 1
        elif c == '-':
            i = 1 if got_pitch else 0
            if off[i] > 1:
                show_context(items, i)
                raise Exception('bad offset')
            off[i] -= 1
        elif c.isnumeric():
            if off[0] or absolute:
                show_context(items, i)
                raise Exception('bad octave notation %s'%s)
            octave = int(c)
            absolute = True
        else:
            show_context(items, i)
            raise Exception("can't parse %s"%s)
    if not got_pitch:
        show_context(items, i)
        raise Exception('no pitch specified in %s'%s)
    if absolute:
        return pitch_class + off[1] + octave*12
    else:
        octave_offset = off[0]
        accidental = off[1]
        pitch_class += accidental
        pitch_class = (pitch_class + 12) % 12
        return next_pitch(cur_pitch, pitch_class, octave_offset)
      
# parse a string of the form c+5
# return pitch index
#
def parse_pitch2(s):
    x = pitch_offset[note_names.index(s[0])]
    octave = 5
    for i in range(1, len(s)):
        c = s[i]
        if c == '-':
            x -= 1
        elif c == '+':
            x += 1
        else:
            octave = int(s[i:])
            break
    n = x + octave*12
    return n
    
# compute pitch specified relative to current pitch.
# If octave_offset is 0,
# return instance of the pitch class closest to the current pitch (tie: upward)
# if it's -1, return the first instance below the current pitch;
# -2, the octave below that etc.
#
def next_pitch(cur_pitch, pitch_class, octave_offset):
    cur_pitch_class = cur_pitch % 12
    cur_octave = cur_pitch // 12
    if octave_offset == 0:
        if pitch_class == cur_pitch_class:
            return cur_pitch
        elif pitch_class < cur_pitch_class:
            diff = cur_pitch_class - pitch_class
            if diff  > 6:
                return pitch_class + 12*(cur_octave+1)
            else:
                return pitch_class + 12*cur_octave
        else:
            diff = pitch_class - cur_pitch_class
            if diff > 6:
                return pitch_class + 12*(cur_octave-1)
            else:
                return pitch_class + 12*cur_octave
    elif octave_offset < 0:
        if pitch_class < cur_pitch_class:
            next_down = pitch_class + 12*cur_octave
        else:
            next_down = pitch_class + 12*(cur_octave-1)
        if octave_offset < -1:
            return next_down  + 12*(octave_offset+1)
        else:
            return next_down
    else:
        if pitch_class > cur_pitch_class:
            next_up = pitch_class + 12*(cur_octave)
        else:
            next_up = pitch_class + 12*(cur_octave+1)
        if octave_offset > 1:
            return next_up + 12*(octave_offset-1)
        else:
            return next_up

def check_pitch(items, i, pitch, time):
    if pitch<0 or pitch>127:
        show_context(items, i)
        raise Exception('illegal pitch %d at time %f'%(pitch, time))
    
# textual note specification
def n(s, mdur=0):
    s = s.replace('[', ' [ ')
    s = s.replace(']', ' ] ')
    ns = nscore.Score()
    cur_pitch = 60
    in_chord = False
    vol = .5
    dur = 1/4
    tags = []
    par = []
    items = s.split()
    ped_start = -1
    ped_start_index = -1
    dt = 0
    items = expand_all(items)
    for i in range(len(items)):
        t = items[i]
        if t == '[':
            if in_chord:
                show_context(items, i)
                raise Exception("Can't nest [")
            in_chord = True
            chord_dur = dur
            tags.append('ch')
        elif t == ']':
            if not in_chord:
                show_context(items, i)
                raise Exception("] not in chord")
            in_chord = False
            ns.advance_time(dur)
            dt += dur
            tags.remove('ch')
        elif t[0] == '|':
            comment(t, dt, mdur)
        elif t == '_':
            ns.advance_time(-dur)
            dt -= dur
        elif '/' in t:
            # rhythm notation
            a = t.split('/')
            try:
                num = int(a[0])
                denom = int(a[1])
            except:
                show_context(items, i)
                raise Exception('bad values in %s'%t)
            d = num/denom
            if in_chord:
                chord_dur = d
            else:
                dur = d
        elif t == '.':
            if in_chord:
                show_context(items, i)
                raise Exception('no rests in chords')
            ns.advance_time(dur)
            dt += dur
        elif t[0] == '(':
            tag = t[1:]
            if tag in tags:
                show_context(items, i)
                raise Exception('tag %s already in effect'%tag)
            tags.append(tag)
        elif t[-1] == ')':
            tag = t[0:-1]
            if tag not in tags:
                show_context(items, i)
                raise Exception('unopened tag %s'%tag)
            tags.remove(tag)
        elif t == 'par':
            if not par:
                show_context(items, i)
                raise Exception('unmatched closing par')
            par.pop()
        elif t[0:3] == 'par':
            par.append(int(t[3:]))
        elif t[0] == '#':
            cur_pitch = parse_pitch2(t[1:])
        elif t == '+p':
            if ped_start >= 0:
                show_context(items, ped_start_index)
                raise Exception('unclosed +p')
            ped_start = ns.cur_time
            ped_start_index = i
        elif t == '-p':
            if ped_start < 0:
                show_context(items, i)
                raise Exception('-p with no matching +p')
            ns.sustain(ped_start, ns.cur_time)
            ped_start = -1
        else:
            # note
            pitch = parse_pitch(items, i, cur_pitch)
            d = chord_dur if in_chord else dur
            check_pitch(items, i, pitch, ns.cur_time)
            ns.append_note(nscore.Note(0, d, pitch, vol, tags))
            for p in par:
                check_pitch(items, i, pitch+p, ns.cur_time)
                ns.append_note(nscore.Note(0, d, pitch+p, vol, tags))
            if not in_chord:
                ns.advance_time(dur)
                dt += dur
            cur_pitch = pitch
    if in_chord:
        raise Exception('unmatched [')
    if par:
        raise Exception('unmatched opening par')
    if ped_start >= 0:
        show_context(items, ped_start_index)
        raise Exception('unclosed +p')
    return ns
