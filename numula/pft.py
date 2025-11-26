# PFT (piecewise function of time) primitives and functions

import math
import cmath
from numula.constants import *

class PFT_Primitive:
    closed_start: bool
    closed_end: bool
    y1: float
    dt: float
    after: bool
    value: float

class Linear(PFT_Primitive):
    def __init__(self,
        y0: float, y1: float, dt: float,
        closed_start=True, closed_end=False
    ):
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.slope = self.dy/self.dt
        self.closed_start = closed_start
        self.closed_end = closed_end
        self.intinv0 = None
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
    def intinv(self, t):
        if self.slope == 0:
            return t/self.y0
        else:
            print(self.slope, t, self.y0)
            return math.log(self.slope*t + self.y0)/self.slope
    def integral_inverse(self, t):
        if self.intinv0 is None:
            self.intinv0 = self.intinv(0)
        x = self.intinv(t) - self.intinv0
        return x
    def delay(self):
        return 0.
    # convert to inverse tempo function
    def invert(self):
        self.y0 = 1/self.y0
        self.y1 = 1/self.y1
        self.dy = self.y1 - self.y0

# for volume PFTs: a period of unity gain
#
def Unity(dt: float):
    return Linear(1, 1, dt)

# for time-shift PFTs: a period of no shift
#
def ZeroSeg(dt: float):
    return Linear(0, 0, dt)

# for volume and time-shift PFTs: a momentary value
#
class Accent(PFT_Primitive):
    def __init__(self, y: float):
        self.y0 = y
        self.y1 = y
        self.closed_start = True
        self.closed_end = True
        self.dt = 0
    def __str__(self):
        return 'Accent %f'%self.y0
    def val(self) -> float:
        return self.y0
    
# An exponential parameterized by "curvature".
# Normalized to 0..1 for both x and y, the value is
# y = (1 - c^x)/(1-c)
# where c is e^curvature
# If curvature > 0 more of the change happens later;
# i.e. if y1 > y0 then the curve is concave up
# and if curvature < 0 more of the change happens earlier.
# If curvature = 0 then y = x; this is handled as a special case
class ExpCurve(PFT_Primitive):
    def __init__(self,
        curvature: float, y0: float, y1: float, dt: float,
        closed_start=True, closed_end=False
    ):
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.slope = self.dy/self.dt
        self.closed_start = closed_start
        self.closed_end = closed_end
        if abs(curvature) < .001:
            self.linear = True
            self.c = 0
            self.ec = 1
        else:
            self.linear = False
            self.c = curvature
            self.ec = math.exp(curvature)
            self.invint0 = None
    def __str__(self):
        return 'ExpCurve: %s %f %f %s, dt %f curvature %f'%(
            '[' if self.closed_start else '(',
            self.y0, self.y1,
            ']' if self.closed_end else ')',
            self.dt, self.c
        )       
    def val(self, t: float) -> float:
        if self.linear:
            return self.y0 + self.dy*(t/self.dt)
        tnorm = t/self.dt
        ynorm = (1 - math.pow(self.ec, tnorm))/(1-self.ec)
        return self.y0 + ynorm*self.dy
    def integral(self, t: float) -> float:
        if self.linear:
            return t*(self.y0+self.val(t))/2
        if t == 0.:
            return 0.
        tnorm = t/self.dt
        num = tnorm*self.c - math.pow(self.ec, tnorm) + 1
        denom = (1-self.ec)*self.c
        int_norm = num/denom
        # convert from normalized coords
        int = t*(self.y0 + int_norm*self.dy)
        #print('integral: ', t, int_norm, self.dy, int)
        return int

    # the indefinite integral of the inverse
    # sources:
    # integral-calculator.com
    # https://wolframalpha.com (alternate form assuming...)
    # they give the same answer
    def invint(self, t):
        ct = math.exp(self.c*t)
        d = self.y0*(self.ec-1) + self.dy*(ct - 1)
        d = math.fabs(d)
        num = (self.ec - 1)*(t*self.c - math.log(d))
        denom = self.c*(self.y0*(self.ec - 1) - self.dy)
        return num/denom

    # definite integral from 0 to t; subtract value at 0
    def integral_inverse(self, t: float) -> float:
        if self.linear:
            return math.log(self.slope*t + self.y0)/self.slope
        if self.intinv0 is None:
            self.intinv0 = self.intinv(0)
        return self.invint(t) - self.invint0

    def delay(self):
        return 0.
    def invert(self):
        self.y0 = 1./self.y0
        self.y1 = 1./self.y1
        self.dy = self.y1 - self.y0

# Used in tempo PFTs to represent pauses
# if after is True, pause goes after notes at that time
class Pause(PFT_Primitive):
    def __init__(self, value: float, after=True):
        self.value = value
        self.after = after
        self.dt = 0.
    def __str__(self):
        return 'Pause %f %s'%(
            self.value,
            'after' if self.after else 'before'
        )
    def invert(self):
        return
    def delay(self):
        return self.value

# a PFT segment whose value is an arbitrary object (e.g. a PitchSet)
#
class PFTObject:
    def __init__(self,
        dt: float, value, closed_start=True, closed_end=False
    ):
        self.dt = dt
        self.y0 = value
        self.y1 = value
        self.closed_start = closed_start
        self.closed_end = closed_end
    def val(self, t: float) -> float:
        return self.y0

# ------------ end of PFT primitives

type PFT = list[PFT_Primitive]

#from pprint import pprint

# Make sure the PFT has well-defined values at segment boundaries
# If the PFT has accents (momentary values) adjust surrounding closures
#
def pft_check_closure(pft):
    n = len(pft)
    t = 0.
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
def pft_dur(pft) -> float:
    dt = 0
    for seg in pft:
        dt += seg.dt
    return dt

# verify that the PFT has the given duration
def pft_verify_dur(pft, dur: float):
    x = pft_dur(pft)
    if x < dur-epsilon:
        raise Exception('PFT is too short: %f < %f'%(x, dur))
    if x > dur+epsilon:
        raise Exception('PFT is too long: %f > %f'%(x, dur))
    
# average value of PFT
def pft_avg(pft) -> float:
    sum = 0.
    for seg in pft:
        if seg.dt == 0: continue
        sum += seg.integral(seg.dt)
    return sum/pft_dur(pft)

# average value of 1/PFT
def pft_inverse_avg(pft) -> float:
    sum = 0.
    for seg in pft:
        if seg.dt == 0: continue
        sum += seg.integral_inverse(seg.dt)
    return sum/pft_dur(pft)

# total delay in a tempo PFT
def pft_delay(pft) -> float:
    sum = 0.
    for seg in pft:
        if seg.dt > 0: continue
        sum += seg.delay()
    return sum

# invert tempo parameters of the PFT's interval primitives
def pft_invert(pft):
    for seg in pft:
        seg.invert()

# class for getting the values of a PFT at increasing times
class PFTValue:
    def __init__(self, pft):
        self.pft = pft
        self.ind = 0            # index of current seg
        self.prev_dur = 0       # duration of previous segs
        self.ended = False
        self.final_value = None

    def value(self, t: float) -> float:
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
def show_pft_vals(pft, dt: float):
    pft_val = PFTValue(pft)
    t = 0.
    last = 0.
    while not pft_val.ended:
        v = pft_val.value(t)
        print(t, v, v-last)
        last = v
        t += dt

# same, but show integral
def show_pft_ints(pft, dt: float):
    for seg in pft:
        print(seg)
        print('total integral ', seg.integral(seg.dt))
        t = 0.
        last = 0
        while t<=seg.dt:
            i = seg.integral(t)
            print(t, i, i-last)
            last = i
            t += dt
