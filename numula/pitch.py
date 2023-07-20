import random
from scipy.stats import norm

# a set of pitch offsets (0..11)
# and an optional set of weights for each one.
# This can represent a chord or scale.
#
class PitchOffs:
    def __init__(self, offsets, probs=None):
        self.offsets = offsets
        if probs:
            self.probs = probs
        else:
            self.probs = [1]*len(offsets)

# the combination of a set of pitch offsets and a root pitch
#
class PitchSet:
    def __init__(self, poffs, root):
        # make an array 0..127 of probabilities
        self.probs = [0]*128
        for i in range(128):
            d = (i-root)%12
            if d in poffs.offsets:
                j = poffs.offsets.index(d)
                self.probs[i] = poffs.probs[j]
            else:
                self.probs[i] = 0
            
    # return a random (uniform but weighted) pitch in lo..hi
    #
    def rnd_uniform(self, lo, hi):
        sum = 0
        for i in range(lo, hi+1):
            sum += self.probs[i]
        x = random.uniform(0, sum)
        y = 0
        for i in range(lo, hi+1):
            if self.probs[i]:
                y += self.probs[i]
                if y > x:
                    return i
        return -1

    # return a random pitch from normal distribution
    #
    def rnd_normal(self, mean, stddev, maxsigma):
        lo = int(mean - stddev*maxsigma)
        hi = int(mean + stddev*maxsigma)
        nprobs = [0]*128
        sum = 0
        for i in range(lo, hi+1):
            if i<0: continue
            if i>127: continue
            nprobs[i] = self.probs[i]*norm.pdf(i, mean, stddev)
            sum += nprobs[i]
        x = random.uniform(0, sum)
        y = 0
        for i in range(lo, hi+1):
            if nprobs[i]:
                y += nprobs[i]
                if y > x:
                    return i
        return -1
    
    # return the pitch in the set above the given pitch
    #
    def next_above(self, p):
        for i in range(1,127):
            j = p+i
            if j>127:
                return -1
            if self.probs[j]:
                return j

    def next_below(self, p):
        for i in range(1, 127):
            j = p-i
            if j<0:
                return -1
            if self.probs[j]:
                return j

