# This file is part of Numula
# Copyright (C) 2024 David P. Anderson
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

# PFT (piecewise function of time) primitives and functions

import math
from numula.constants import *

class Linear:
    def __init__(self, y0, y1, dt, closed_start=True, closed_end=False):
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.closed_start = closed_start
        self.closed_end = closed_end
    def __str__(self):
        return 'Linear: %s %f %f %s, dt %f'%(
            '[' if self.closed_start else '(',
            self.y0, self.y1,
            ']' if self.closed_end else ')',
            self.dt
        )
    def val(self, t):
        return self.y0 + self.dy*(t/self.dt)
    def integral(self, t):
        return t*(self.y0+self.val(t))/2
    def integral_total(self):
        return self.dt*(self.y0+self.y1)/2
    def delay(self):
        return 0
    # convert from tempo function in BPM (60-centered)
    # to 1-centered inverse tempo function
    def bpm(self):
        self.y0 = 60/self.y0
        self.y1 = 60/self.y1
        self.dy = self.y1 - self.y0

# for volume PFTs: a period of unity gain
#
def Unity(dt):
    return Linear(1, 1, dt)

# for time-shift PFTs: a period of no shift
#
def ZeroSeg(dt):
    return Linear(0, 0, dt)

# for volume and time-shift PFTs: a momentary value
#
class Accent:
    def __init__(self, y):
        self.y0 = y
        self.y1 = y
        self.closed_start = True
        self.closed_end = True
        self.dt = 0
    def __str__(self):
        return 'Accent %f'%self.y0
    def val(self, t):
        return y0
    
# An exponential parameterized by "curvature".
# Normalized to 0..1 for both x and y, the value is
# y = (1 - c^x)/(1-c)
# where c is e^curvature
# If curvature > 0 more of the change happens later;
# i.e. if y1 > y0 then the curve is concave up
# and if curvature < 0 more of the change happens earlier.
# If curvature = 0 then y = x; this is handled as a special case
class ExpCurve:
    def __init__(self, curvature, y0, y1, dt, closed_start=True, closed_end=False):
        if abs(curvature) < .001:
            self.linear = True
        else:
            self.linear = False
            self.c = math.exp(curvature)
            self.logc = curvature
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.closed_start = closed_start
        self.closed_end = closed_end
        self.curvature = curvature
    def __str__(self):
        return 'ExpCurve: %s %f %f %s, dt %f curvature %f'%(
            '[' if self.closed_start else '(',
            self.y0, self.y1,
            ']' if self.closed_end else ')',
            self.dt, self.curvature
        )       
    def val(self, t):
        if self.linear:
            return self.y0 + self.dy*(t/self.dt)
        tnorm = t/self.dt
        ynorm = (1 - math.pow(self.c, tnorm))/(1-self.c)
        return self.y0 + ynorm*self.dy
    def integral(self, t):
        if self.linear:
            return t*(self.y0+self.val(t))/2
        if t == 0:
            return 0
        # I assume you know that the integral of a^x is a^x/ln(a) + C
        # (OK, so I had to look it up)
        #
        tnorm = t/self.dt

        a = (math.pow(self.c, tnorm) - 1)/self.logc

        int_norm = (tnorm-a)/(1-self.c)

        # convert from normalized coords
        int = t*(self.y0 + int_norm*self.dy)
        #print('integral: ', t, int_norm, self.dy, int)
        return int
    def integral_total(self):
        if self.linear:
            return self.dt*(self.y0+self.y1)/2
        return self.integral(self.dt)
    def delay(self):
        return 0
    def bpm(self):
        self.y0 = 60/self.y0
        self.y1 = 60/self.y1
        self.dy = self.y1 - self.y0

# Dirac delta; used in tempo PFTs to represent pauses
# if after is True, pause goes after notes at that time
class Delta:
    def __init__(self, value, after=True):
        self.value = value
        self.after = after
        self.dt = 0
    def __str__(self):
        return 'Delta %f %s'%(
            self.value,
            'after' if self.after else 'before'
        )
    def bpm(self):
        return
    def integral_total(self):
        return 0
    def delay(self):
        return self.value

# a pedal PFT is a list of these.
# level 0 is a period of no pedal
# pedal types don't have to all be the same
class PedalSeg:
    def __init__(self, dt, level, pedal_type=pedal_sustain):
        self.dt = dt
        self.level = level
        self.pedal_type = pedal_type
    def __str__(self):
        return 'PedalSeg: dt %f type %d level %f'%(
            self.dt, self.pedal_type, self.level
        )

# a PFT segment whose value is an arbitrary object (e.g. a PitchSet)
#
class PFTObject:
    def __init__(self, dt, value, closed_start=True, closed_end=False):
        self.dt = dt
        self.y0 = value
        self.y1 = value
        self.closed_start = closed_start
        self.closed_end = closed_end
    def val(self, t):
        return self.y0

# ------------ end of PFT primitives

#from pprint import pprint

# make sure the pft has well-defined values at segment boundaries
def pft_check_closure(pft):
    n = len(pft)
    t = 0
    for i in range(n-1):
        seg0 = pft[i]
        t += seg0.dt
        seg1 = pft[i+1]
        if isinstance(seg0, Accent):
            seg1.closed_start = False
            continue
        if isinstance(seg1, Accent):
            seg0.closed_end = False
            continue
        if seg0.closed_end:
            if seg1.closed_start and seg0.y1 != seg1.y0:
                raise Exception('conflicting values in PFT at time %f'%t)
        else:
            if not seg1.closed_start:
                raise Exception('missing value in PFT at time %f'%t)

# score-time duration of a PFT
def pft_dur(pft):
    dt = 0
    for seg in pft:
        dt += seg.dt
    return dt

# verify that the PFT has the given duration
def pft_verify_dur(pft, dur):
    x = pft_dur(pft)
    if x < dur-epsilon:
        raise Exception('PFT is too short: %f < %f'%(x, dur))
    if x > dur+epsilon:
        raise Exception('PFT is too long: %f > %f'%(x, dur))
    
# average value of pft
def pft_avg(pft):
    sum = 0
    for seg in pft:
        sum += seg.integral_total()
    return sum/pft_dur(pft)

# total delay in tempo PFT
def pft_delay(pft):
    sum = 0
    for seg in pft:
        sum += seg.delay()
    return sum

# convert tempo PFT from BPM units
def pft_bpm(pft):
    for seg in pft:
        seg.bpm()

# class for getting the values of a PFT at increasing times
class PFTValue:
    def __init__(self, pft):
        self.pft = pft
        self.ind = 0            # index of current seg
        self.prev_dur = 0       # duration of previous segs
        self.ended = False

    def value(self, t):
        if self.ended:
            return self.final_value
        dt = t - self.prev_dur
        while True:
            seg = self.pft[self.ind]
            if dt < seg.dt - epsilon:
                return seg.val(dt)
            if dt < seg.dt + epsilon and seg.closed_end:
                return seg.y1
            dt -= seg.dt
            self.prev_dur += seg.dt
            self.ind += 1
            if self.ind == len(self.pft):
                self.ended = True
                self.final_value = seg.y1
                return self.final_value
            
# show PFT values with given spacing (for debugging)
def show_pft_vals(pft, dt):
    pft_val = PFTValue(pft)
    t = 0
    last = 0
    while not pft_val.ended:
        v = pft_val.value(t)
        print(t, v, v-last)
        last = v
        t += dt

# same, but show integral
def show_pft_ints(pft, dt):
    for seg in pft:
        print(seg)
        print('total integral ', seg.integral_total())
        t = 0
        last = 0
        while t<=seg.dt:
            i = seg.integral(t)
            print(t, i, i-last)
            last = i
            t += dt
