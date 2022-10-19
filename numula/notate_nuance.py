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

import numula.nscore
from numula.nuance import *
from numula.notate import *
from numula.vol_name import *

# continuous volume change
# e.g.: 'Linear *2 f 1/4 pp ] mp 2/4 p *'
# means: go from f to pp over 1/4 (closed at end)
# then go from mp to p over 2/4
# repeat this twice

vol_name = {
    'pppp': pppp,
    'pppp_': pppp_,
    '_ppp': _ppp,
    'ppp': ppp,
    'ppp_': ppp_,
    '_pp': _pp,
    'pp': pp,
    'pp_': pp_,
    '_p': _p,
    'p': p,
    'p_': p_,
    '_mp': _mp,
    'mp': mp,
    'mp_': mp_,
    'mm': mm,
    '_mf': _mf,
    'mf': mf,
    'mf_': mf_,
    '_f': _f,
    'f': f,
    'f_': f_,
    '_ff': _ff,
    'ff': ff,
    'ff_': ff_,
    '_fff': _fff,
    'fff': fff,
    'fff_': fff_,
    '_ffff': _ffff,
    'ffff': ffff

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

def vol(s, mdur=0):
    items = s.split()
    items = expand_all(items)
    state = INIT
    pft = []
    last_seg = None
    got_rb = False
    got_lb = False
    segtype = SEGTYPE_LINEAR
    dt = 0
    for i in range(len(items)):
        t = items[i]
        if t[0] == '|':
            comment(t, dt, mdur)
        elif '/' in t:
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
        elif t == 'linear':
            segtype = SEGTYPE_LINEAR
        elif t[0:3] == 'exp':
            segtype = SEGTYPE_EXP
            try:
                curvature = float(t[3:])
            except:
                show_context(items, i)
                raise Exception('bad curvature')
        else:
            if t in vol_keys:
                v = vol_name[t]
            else:
                try:
                    v = float(t)
                except:
                    show_context(items, i)
                    raise Exception('unrecognized item')
            if state == INIT or state == GOT_V0:
                v0 = v
                state = GOT_V0
            elif state == GOT_DUR:
                v1 = v
                if not got_lb and not got_rb and last_seg and last_seg.y1 != v0:
                    show_context(items, i)
                    raise Exception('Inconsistent values: %f and %f'%(last_seg.y1, v0))
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
                dt += dur
            elif state == GOT_V1:
                if v != v0 and not got_rb and not got_lb:
                    show_context(items, i)
                    raise Exception('inconsistent volumes')
                v0 = v
                state = GOT_V0
    pft_check_closure(pft)
    return pft

#x = vol('pp 1/4 mf [ exp3 ppp 1/2 pp')
#x = vol('pp 1/4 p 3/4 pp [ p   1/4 p 3/4 pp')
#print(*x, sep='\n')

# e.g. '1/8 1.2 1/4 1.2 1/4 1.2 1/8'

def accents(s, mdur=0):
    items = s.split()
    items = expand_all(items)
    dt = 0
    pft = []
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
            dt += dur
        elif t[0] == '|':
            comment(t, dt, mdur)
        else:
            if t in vol_keys:
                v = vol_name[t]
            else:
                try:
                    v = float(t)
                except:
                    show_context(items, i)
                    raise Exception('unrecognized item')
            pft.append(Accent(v))
    return pft

#x = accents('1/8 1.2 1/4 1.3 1/2')
#print(*x, sep='\n')

# e.g.: 'linear 60 8/4 80 p0.1 60 3/4 120 0.2p'

def tempo(s, mdur=0):
    items = s.split()
    items = expand_all(items)
    pft = []
    t0 = None
    dur = None
    dt = 0
    segtype = SEGTYPE_LINEAR
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
        elif t[0] == '|':
            comment(t, dt, mdur)
        elif t == 'linear':
            segtype = SEGTYPE_LINEAR
        elif t[0:3] == 'exp':
            segtype = SEGTYPE_EXP
            try:
                curvature = float(t[3:])
            except:
                show_context(items, i)
                raise Exception('bad curvature')
        elif t[0] == 'p':
            try:
                val = float(t[1:])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=True))
        elif t[-1] == 'p':
            try:
                val = float(t[0:-1])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=False))
        elif 'p' in t:
            pos = t.index('p')
            try:
                val = float(t[0:pos])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=False))
            try:
                val = float(t[pos+1:])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(Delta(val, after=True))
        else:
            # parse a tempo
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
                dt += dur
                dur = None
            t0 = val
    return pft

#x = tempo('*2 60 8/4 80 p.01 60 3/4 120 0.2p *')
#print(*x, sep='\n')

# e.g. '- 1/4 + 1/8 + 1/4 - 4/4'
def pedal(s, mdur=1, pedal_type=pedal_sustain):
    items = s.split()
    items = expand_all(items)
    pft = []
    on = False
    dt = 0
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
            dt += dur
        elif t[0] == '|':
            comment(t, dt, mdur)
        elif t == '-':
            on = False
        elif t == '+':
            on = True
    return pft

#x = pedal('- 1/4 + 1/8 + 1/4 - 4/4')
#print(*x, sep='\n')
