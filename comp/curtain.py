import random
from numula.nscore import *
from numula.nuance import *

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
