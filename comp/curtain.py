import random
from numula.nscore import *
from numula.nuance import *

# a PitchSet whose 'weight' (probability of using it)
# changes over time
class HarmonyShape:
    def __init__(self, ps, t0, weight):
        self.ps = ps
        self.start = t0
        self.end = t0 + pft_dur(weight)
        self.weight = weight

# a collection of Harmony Shapes,
# with logic for picking one to use at a particular time
class HarmonyShapeSet:
    def __init__(self, shapes):
        for s in shapes:
            s.pftval = PFTValue(s.weight)
        self.inactive = shapes
        self.active = []

    # which PitchSet to use at time t
    #
    def value(self, t):
        for s in self.active:
            if t > s.end:
                self.active.remove(s)
        for s in self.inactive:
            if t >= s.start:
                self.inactive.remove(s)
                if t <= s.end:
                    self.active.append(s)
        if not self.active:
            print('nothing active at ', t)
            return None
        tw = 0
        for s in self.active:
            s.w = s.pftval.value(t-s.start)
            tw += s.w
        x = random.uniform(0, 1)*tw
        for s in self.active:
            x -= s.w
            if x <=0:
                return s.ps
        raise Exception('should not reach here')

def cloud(
    times,      # list of note times
    hss,        # HarmonyShapeSet
    center,     # PFT for pitch center
    width,      # PFT for pitch width
    cycle,      # 0 means uniform random
    no_repeat   # bool
):
    ns = Score()
    center_val = PFTValue(center)
    width_val = PFTValue(width)
    last = int(center_val.value(0))
    for t in times:
        c = int(center_val.value(t))
        w = int(width_val.value(t))
        lo = c - w
        hi = c + w
        ps = hss.value(t)
        if not ps:
            continue
        print('using ', ps.name, ' at time ', t)
        if cycle == 0:
            i = ps.rnd_uniform(lo, hi)
            if no_repeat and i == last:
                i = ps.gt(i)
        else:
            i = last + cycle
            if i > hi:
                i -= w
            if i < lo:
                i += w
            i = ps.ge(i)
        last = i
        ns.insert_note(Note(t, 1, i, .2))
    return ns
        
    
# times: sorted list of times
# pitch_set: pitch set PFT
# pitch_center: center of pitch interval (PFT)
# pitch_width: size of pitch interval (PFT)
#
# You can then apply volume and timing
#
def curtain(
    times, pitch_set, pitch_center, pitch_width, no_rep=False, gaussian=False
):
    psval = PFTValue(pitch_set)
    pcval = PFTValue(pitch_center)
    pwval = PFTValue(pitch_width)
    ns = Score()
    prev_pitch = 0
    for t in times:
        ps = psval.value(t)
        pc = pcval.value(t)
        pw = pwval.value(t)
        if gaussian:
            pitch = ps.rnd_normal(pc, pw, 2)
        else:
            pitch = ps.rnd_uniform(int(pc-pw), int(pc+pw))
        if pitch < 0:
            print('bad pitch ', pc, pw)
        if no_rep:
            while pitch == prev_pitch:
                pitch = ps.rnd_uniform(int(pc-pw), int(pc+pw))
            prev_pitch = pitch
        ns.insert_note(Note(t, 1, pitch, .2))
    return ns
