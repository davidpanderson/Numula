from comp.pitch import *
from comp.time_list import *
from comp.curtain import *
from numula.nscore import *
from numula.nuance import *
from numula.notate_nuance import *
import numula.pianoteq as pianoteq

# play a scale
def scale(ps: PitchSet, durs: list[int], vols: list[float], lo: int, hi: int):
    p = ps.ge(lo, 0)
    ns = ScoreBasic()
    while True:
        index = ps.index[p]
        d = durs[index]
        v = vols[index]
        ns.append_note(Note(0, d, p, .7*v))
        if p > hi and ps.index[p] == 0:
            break;
        p = ps.gt(p)
        ns.advance_time(d)
    return ns

def test_scale():
    durs = [1/12]+[1/24]*6
    vols = [1,.6,.8,.6,.85,.6, .6]
    ps = PitchSet(melodic_minor, 60)
    ns = scale(ps, durs, vols, 20, 100);
    pianoteq.play_score(ns)

test_scale()

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
        sh_vol('20 4/1 20')
    )
    hs2 = HarmonyShape(ps2, 1/2,
        sh_vol('0 1/2 100 1/1 100 1/2 0')
    )
    hs3 = HarmonyShape(ps3, 3/2,
        sh_vol('0 1/2 100 1/1 100 1/2 0')
    )
    ns = cloud(
        time_list_pft(sh_vol('40 4/1 40'), False),
        HarmonyShapeSet([hs1, hs2, hs3]),
        sh_vol('60 4/1 60'),
        sh_vol('36 4/1 24'),
        0,
        True
    );
    pianoteq.play_score(ns)

#test_cloud()
                      
