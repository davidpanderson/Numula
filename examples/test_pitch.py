from numula.pitch import *
from curtain import *
from numula.nscore import *
from numula.nuance import *
import numula.pianoteq as pianoteq

def test_pitch():
    maj = PitchOffs([0,4,7])
    cmaj = PitchSet(maj, 60)
    #print(cmaj.probs)
    for i in range(10):
        print(cmaj.rnd_uniform(40, 80))
#test_pitch()

def test_curtain():
    maj = PitchOffs([0, 4, 7])
    minor = PitchOffs([0, 3, 7])
    cmaj = PitchSet(maj, 60)
    cmin = PitchSet(minor, 60)
    pitch_set = [
        PFTObject(4, cmaj),
        PFTObject(4, cmin)
    ]
    pitch_center = [
        Linear(60, 80, 6),
        Linear(80, 60, 2)
    ]
    pitch_width = [
        Linear(20, 30, 8)
    ]
    ns = curtain(8, 300, pitch_set, pitch_center, pitch_width, False)
    pianoteq.play_score(ns)
test_curtain()
