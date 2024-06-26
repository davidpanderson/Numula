# functions involving lists of times

# TODO: support variable rates (how?)

import random
from numula.nscore import *
from numula.nuance import *

# generate a time list from a PFT of note density (notes per measure)
#
def time_list_pft(pft, is_random):
    t = 0
    tlist = [0]
    val = PFTValue(pft)
    end = pft_dur(pft)
    while True:
        x = val.value(t)
        if is_random:
            t += exp(-x)
        else:
            t += 1/x
        if t > end: break
        tlist.append(t)
    return tlist
        
def time_list_periodic(n, dur):
    tl = []
    dt = dur/n
    for i in range(n):
        tl.append(i*dt)
    return tl

# random times in given range
def time_list_random(n, dur):
    tl = []
    for i in range(n):
        tl.append(random.uniform(0,dur))
    tl.sort()
    return tl

# time separation is uniformly random
def time_list_random_sep(n, lo, hi):
    tl = [0]
    for i in range(1, n):
        dt = random.uniform(lo, hi)
        tl.append(tl[i-1]+dt)
    return tl

# scale times
def time_list_scale(tlist, dur):
    scale = dur/tlist[len(tlist)-1]
    for i in range(len(tlist)):
        tlist[i] *= scale

# snap to grid
def time_list_snap(tlist, dt):
    for i in range(len(tlist)):
        tlist[i] = dt*int(tlist[i]/dt)
