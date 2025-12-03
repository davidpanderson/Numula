import numula_path
from numula.nscore import *
from numula.notate_nuance import *
from numula.pianoteq import *

def cycle(
    bottom: PFT,
    top: PFT,
    incr: PFT,
    vol: PFT,
    dtgen
):
    ns = Score()
    t = 0
    p = bottom.value(t)
    dur = pft_dur(bottom.pft)

    while t <= dur:
        dt = next(dtgen)
        ns.insert_note(Note(t, dt*2, int(p), vol.value(t)/2))
        t += dt
        inc = incr.value(t)
        bt = bottom.value(t)
        tp = top.value(t)
        p += inc
        diff = tp - bt
        if p > top.value(t):
            while p-diff > bt:
                p -= diff
        #print('top', tp, 'bottom', bt, 't', t, 'p', p, 'incr', inc)
    return ns

def dtgen():
    while True:
        for i in range(4):
            yield 1/32
        for i in range(3):
            yield 1/24

def test_cycle():
    dts = dtgen()
    ns = cycle(
        PFTValue(sh_vol('45 12/1 40')),
        PFTValue(sh_vol('55 12/1 80')),
        PFTValue(sh_vol('7 12/1 31')),
        PFTValue(sh_vol('pp 6/1 ff 6/1 pp')),
        dts
    )
    #print(ns)
    numula.pianoteq.play_score(ns)
    
test_cycle()
