# Textual notation of nuance.
# see https://github.com/davidpanderson/Numula/wiki/nuance_notate.py

import nscore
from nuance import *
from notate import *

# continuous volume change
# e.g.: 'linear *2 f 1/4 pp ] mp 2/4 p *'
# means: go from f to pp over 1/4 (closed at end)
# then go from mp to p over 2/4
# repeat this twice

vol_name = {
    'ppp': ppp,
    'pp': pp,
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
        items = expand(items)
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
            if state != GOT_V1:
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
            if state == INIT:
                v0 = v
                state = GOT_V0
            elif state == GOT_V0:
                show_context(items, i)
                raise Exception('unexpected volume')
            elif state == GOT_DUR:
                v1 = v
                if segtype == SEGTYPE_LINEAR:
                    last_seg = linear(v0, v1, dur, closed_end=True)
                else:
                    last_seg = exp_curve(curvature, v0, v1, dur, closed_end=True)
                if got_lb:
                    last_seg.closed_start = True
                    got_lb = False
                if got_rb:
                    last_seg.closed_start = False
                    got_rb = False
                pft.append(last_seg)
                v0 = v1
                state = GOT_V1
            elif state == GOT_V1:
                if v != v0 and not got_rb and not got_lb:
                    show_context(items, i)
                    raise Exception('inconsistent volumes')
                v0 = v
                state = GOT_V0
    return pft

x = vol('pp 1/4 mf [ exp3 ppp 1/2 pp')
print(*x, sep='\n')

# e.g. '1/8 1.2 1/4 1.2 1/4 1.2 1/8'

def accents(s):
    items = s.split()
    pft = []
    if '*' in items:
        items = expand(items)
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
            pft.append(unity(dur))
        elif t[0] == '|':
            continue
        else:
            try:
                val = float(t)
            except:
                show_context(items, i)
                raise Exception('bad value')
            pft.append(accent(val))
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
        items = expand(items)
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
            pft.append(delta(val, after=False))
        elif t[-1] == 'p':
            try:
                val = float(t[0:-1])
            except:
                show_context(items, i)
                raise Exception('bad pause value')
            pft.append(delta(val, after=True))
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
                    seg = linear(t0, val, dur)
                else:
                    seg = exp_curve(curvature, t0, val, dur)
                pft.append(seg)
                dur = None
            t0 = val
    return pft

#x = tempo('*2 60 8/4 80 p.01 60 3/4 120 0.2p *')
#print(*x, sep='\n')
