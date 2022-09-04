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


# Textual notation of nuance.
# see https://github.com/davidpanderson/Numula/wiki/nuance_notate.py

import nscore
from nuance import *
from notate import *

# continuous volume change
# e.g.: 'Linear *2 f 1/4 pp ] mp 2/4 p *'
# means: go from f to pp over 1/4 (closed at end)
# then go from mp to p over 2/4
# repeat this twice

vol_name = {
    'ppp': ppp,
    'pp': pp,
    'p': p,
    'mp': mp,
    'mf': mf,
    'f': f,
    'ff': ff,
    'fff': fff
}

vol_keys = vol_name.keys()

SEGTYPE_LINEAR = 0
SEGTYPE_EXP = 1

# parse states for vol()
INIT = 0
GOT_V0 = 1
GOT_DUR = 2
GOT_V1 = 3
GOT_LB = 4
GOT_RB = 5

def vol(s):
    items = s.split()
    if '*' in items:
        items = expand_iter(items)
    state = INIT
    pft = []
    last_seg = None
    got_rb = False
    got_lb = False
    segtype = SEGTYPE_LINEAR
    
    for i in range(len(items)):
        t = items[i]
        if '/' in t:
            if state != GOT_V0:
                show_context(items, i)
                raise Exception('unexpected duration')
            a = t.split('/')
            try:
                num = int(a[0])
                denom = int(a[1])
            except:
                show_context(items, i)
                raise Exception('bad values in %s'%t)
            dur = num/denom
            state = GOT_DUR
        elif t == ']':
            if state != GOT_V0:
                show_context(items, i)
                raise Exception('unexpected ]')
            last_seg.closed_end = True
            got_rb = True
        elif t == '[':
            if last_seg:
                last_seg.closed_end = False
            state = INIT
            got_lb = True
        elif t[0] == '|':
            continue
        elif t == 'linear':
            segtype = SEGTYPE_LINEAR
        elif t[0:3] == 'exp':
            segtype = SEGTYPE_EXP
            try:
                curvature = float(t[3:])
            except:
                show_context(items, i)
                raise Exception('bad curvature')
        elif '.' in t or t in vol_keys:
            if '.' in t:
                v = float(t)
            else:
                v = vol_name[t]
            if state == INIT or state == GOT_V0:
                v0 = v
                state = GOT_V0
            elif state == GOT_DUR:
                v1 = v
                if segtype == SEGTYPE_LINEAR:
                    last_seg = Linear(v0, v1, dur, closed_end=True)
                else:
                    last_seg = ExpCurve(curvature, v0, v1, dur, closed_end=True)
                if got_lb:
                    last_seg.closed_start = True
                    got_lb = False
                if got_rb:
                    last_seg.closed_start = False
                    got_rb = False
                pft.append(last_seg)
                v0 = v1
                state = GOT_V0
            elif state == GOT_V1:
                if v != v0 and not got_rb and not got_lb:
                    show_context(items, i)
                    raise Exception('inconsistent volumes')
                v0 = v
                state = GOT_V0
        else:
            show_context(items, i)
            raise Exception('unrecognized item')
    pft_check_closure(pft)
    return pft

#x = vol('pp 1/4 mf [ exp3 ppp 1/2 pp')
#x = vol('pp 1/4 p 3/4 pp [ p   1/4 p 3/4 pp')
#print(*x, sep='\n')

# e.g. '1/8 1.2 1/4 1.2 1/4 1.2 1/8'

def accents(s):
    items = s.split()
    pft = []
    if '*' in items:
        items = expand_iter(items)
    for i in range(len(items)):
        t = items[i]
        if '/' in t:
            a = t.split('/')
            try:
                num = int(a[0])
                denom = int(a[1])
            except:
                show_context(items, i)
                raise Exception('bad values in %s'%t)
            dur = num/denom
            pft.append(Unity(dur))
        elif t[0] == '|':
            continue
        else:
            try:
                val = float(t)
            except:
                show_context(items, i)
                raise Exception('bad value')
            pft.append(Accent(val))
    return pft

#x = accents('1/8 1.2 1/4 1.3 1/2')
#print(*x, sep='\n')

# e.g.: 'linear 60 8/4 80 p0.1 60 3/4 120 0.2p'

def tempo(s):
    items = s.split()
    pft = []
    t0 = None
    dur = None
    segtype = SEGTYPE_LINEAR
    if '*' in items:
        items = expand_iter(items)
    for i in range(len(items)):
        t = items[i]
        if '/' in t:
            if t0 == None:
                show_context(items, i)
                raise Exception('missing tempo')
            a = t.split('/')
            try:
                num = int(a[0])
                denom = int(a[1])
            except:
                show_context(items, i)
                raise Exception('bad values in %s'%t)
            dur = num/denom
        elif t[0] == 'p':
            try:
                val = float(t[1:])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=False))
        elif t[-1] == 'p':
            try:
                val = float(t[0:-1])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=True))
        elif t == 'linear':
            segtype = SEGTYPE_LINEAR
        elif t[0:3] == 'exp':
            segtype = SEGTYPE_EXP
            try:
                curvature = float(t[3:])
            except:
                show_context(items, i)
                raise Exception('bad curvature')
        elif t[0] == '|':
            continue
        else:
            try:
                val = float(t)
            except:
                show_context(items, i)
                raise Exception('bad value')
            if dur != None:
                if segtype == SEGTYPE_LINEAR:
                    seg = Linear(t0, val, dur)
                else:
                    seg = ExpCurve(curvature, t0, val, dur)
                pft.append(seg)
                dur = None
            t0 = val
    return pft

#x = tempo('*2 60 8/4 80 p.01 60 3/4 120 0.2p *')
#print(*x, sep='\n')

# e.g. '- 1/4 + 1/8 + 1/4 - 4/4'
def pedal(s):
    items = s.split()
    pft = []
    pedal_type = pedal_sustain
    on = False
    if '*' in items:
        items = expand_iter(items)
    for i in range(len(items)):
        t = items[i]
        if '/' in t:
            a = t.split('/')
            try:
                num = int(a[0])
                denom = int(a[1])
            except:
                show_context(items, i)
                raise Exception('bad values in %s'%t)
            dur = num/denom
            if on:
                pft.append(PedalSeg(dur, 1, pedal_type))
            else:
                pft.append(PedalSeg(dur, 0, pedal_type))      
        elif t == '-':
            on = False
        elif t == '+':
            on = True
    return pft

#x = pedal('- 1/4 + 1/8 + 1/4 - 4/4')
#print(*x, sep='\n')
