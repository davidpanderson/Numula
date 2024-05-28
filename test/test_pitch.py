from comp.pitch import *
from comp.time_list import *
from comp.curtain import *
from numula.nscore import *
from numula.nuance import *
from numula.notate_nuance import *
import numula.pianoteq as pianoteq

def test_pitch():
    maj = PitchOffs([0,4,7])
    cmaj = PitchSet(maj, 60)
    print(cmaj.probs)
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
    times = time_list_periodic(400, 12)
    #times = time_list_random(300, 12)
    ns = curtain(times, pitch_set, pitch_center, pitch_width, True, True)
    pianoteq.play_score(ns)
#test_curtain()

# 4-measure cloud with
# - a background chromatic pitchset of weight 1
# - a C chord: .5/0 - 1./100  - 2.0/100 - 2.5/0
# - an F# chord: 1.5/0 - 2.0/100 - 3.0/100 - 3.5/0
#
def test_cloud():
    ps1 = PitchSet(PitchOffs(chromatic), 0, 'chromatic')
    ps2 = PitchSet(PitchOffs(major_triad), 0, 'C maj')
    ps3 = PitchSet(PitchOffs(major_triad), 6, 'F# maj')

    hs1 = HarmonyShape(ps1, 0,
        vol('20 4/1 20')
    )
    hs2 = HarmonyShape(ps2, 1/2,
        vol('0 1/2 100 1/1 100 1/2 0')
    )
    hs3 = HarmonyShape(ps3, 3/2,
        vol('0 1/2 100 1/1 100 1/2 0')
    )
    ns = cloud(
        time_list_pft(vol('40 4/1 40'), False),
        HarmonyShapeSet([hs1, hs2, hs3]),
        vol('60 4/1 60'),
        vol('36 4/1 24'),
        0,
        True
    );
    pianoteq.play_score(ns)

test_cloud()
                      
