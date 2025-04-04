import random
from scipy.stats import norm

# lists of pitch offsets (0..11) are used to define scales and chords

major_scale     = [0,2,4,5,7,9,11]
natural_minor   = [0,2,3,5,7,8,10]
harmonic_minor  = [0,2,3,5,7,8,11]
melodic_minor   = [0,2,3,5,7,9,11]
major_triad     = [0,4,7]
minor_triad     = [0,3,7]
dim_chord       = [0,3,6,9]
chromatic       = [0,1,2,3,4,5,6,7,8,9,10,11]

# probability weights that emphasize root/3rd/5th of 7-note scales
triad_weights = [1,.5,.8,.5,.85,.5, .5]

# the combination of a set of pitch offsets and a root pitch
# Can specify a list of probabilities for random pitch selection
#
class PitchSet:
    def __init__(self,
        poffs: list[int],
        root: int,
        probs: list[float] = None,
        name: str = ''
    ):
        probs = probs if probs else [1]*len(poffs)
        self.name = name
        # make an array 0..127 of probabilities
        self.probs = [0]*128
        self.index = [0]*128     # index in pitch offset list
        self.poffs_len = len(poffs)
        for i in range(128):
            d = (i-root)%12
            if d in poffs:
                j = poffs.index(d)
                self.probs[i] = probs[j]
                self.index[i] = j
            else:
                self.probs[i] = 0
            
    # return a random (uniform but weighted) pitch in lo..hi
    #
    def rnd_uniform(self, lo: int, hi: int):
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
    def rnd_normal(self, mean: float, stddev: float, maxsigma: float):
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

    # return next pitch above/below a given pitch
    # doesn't take probabilities into account
    #
    def gt(self, p: int, index: int = -1):
        i = p
        while True:
            i += 1
            if i > 127: return 0
            if self.probs[i] == 0: continue
            if index >= 0 and self.index[i] != index: continue
            return i

    def ge(self, p: int, index: int = -1):
        return self.gt(p-1, index)
    def lt(self, p: int, index: int = -1):
        i = p
        while True:
            i -= 1
            if i < 1: return 0;
            if self.probs[i] == 0: continue
            if index >= 0 and self.index[i] != index: continue            
            return i
    def le(self, p: int, index: int = -1):
        return self.lt(i+1, index)

# return the number of pitches not common between two PitchSets
#
def pitch_set_distance(ps1, ps2):
    sum = 0
    for i in range(12):
        if ps1.probs[i]==0: continue
        if ps2.probs[i]==0: continue
        sum += 1
    return 12-sum
