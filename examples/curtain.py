import random
from numula.nscore import *
from numula.nuance import *

# dur: duration (measures)
# nnotes: # of notes
# pitch_set: pitch set PFT
# pitch_center: center of pitch interval (PFT)
# pitch_width: size of pitch interval (PFT)
#
# You can then apply volume and timing PFT.
#
def curtain(dur, nnotes, pitch_set, pitch_center, pitch_width, rnd_times):
    # make a list of note times
    times = [0]*nnotes
    for i in range(nnotes):
        if rnd_times:
            times[i] = random.uniform(0, dur)
        else:
            times[i] = (dur*i)/nnotes
    times.sort()
    psval = PFTValue(pitch_set)
    pcval = PFTValue(pitch_center)
    pwval = PFTValue(pitch_width)
    ns = Score()
    for t in times:
        ps = psval.value(t)
        pc = pcval.value(t)
        pw = pwval.value(t)
        pitch = ps.rnd_uniform(int(pc-pw), int(pc+pw))
        if pitch < 0:
            print('bad pitch ', pc, pw)
        ns.insert_note(Note(t, 1, pitch, .2))
    return ns
