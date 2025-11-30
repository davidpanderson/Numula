import numula_path
from numula.nscore import *
from numula.notate_nuance import *

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
        ns.insert_note(Note(t, dt, int(p), vol.value(t)/2))
        t += dt
        p += incr.value(t)
        if p > top.value(t):
            p = bottom.value(t)
    return ns

def dtgen():
    while True:
        yield 1/8
        yield 1/8
        yield 1/4

def test_cycle():
    dts = dtgen()
    ns = cycle(
        PFTValue(sh_vol('40 12/1 30')),
        PFTValue(sh_vol('50 12/1 80')),
        PFTValue(sh_vol('7 12/1 7')),
        PFTValue(sh_vol('mf 12/1 f')),
        dts
    )
    print(ns)
    numula.pianoteq.play_score(ns)
    
test_cycle()
