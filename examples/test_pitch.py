from numula.pitch import *
from numula.time_list import *
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
    #cmin = PitchSet(minor, 60)
    pitch_set = []
    for i in range(12):
        po = PitchSet(random.choice([maj, minor]), random.randrange(0,12))
        pitch_set.append(PFTObject(1, po))
    pitch_center = [
        Linear(85,65, 6),
        Linear(65,85, 6)
    ]
    pitch_width = [
        Linear(10,15, 12)
    ]
    times = time_list_periodic(300, 12)
    #times = time_list_random(300, 12)
    ns = curtain(times, pitch_set, pitch_center, pitch_width, True, True)
    pianoteq.play_score(ns)
test_curtain()
