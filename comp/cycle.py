import numula_path
from numula.nscore import *
from numula.notate_nuance import *

def cycle(
    bottom: PFT,
    top: PFT,
    incr: PFT,
    vol: PFT,
    dt
):
    ns = Score()
    t = 0
    p = bottom.value()

    while True:
        ns.append_note(Note(t, int(p), vol.value(t)))
        t += dt.next();
        p += incr.value(t)
        if p > top.value(t):
            p = bottom.value(t)
    return ns

def tgen():
    while True:
        yield 1/8
        yield 1/8
        yield 1/4

def test_cycle():
    ns = cycle(
        sh_value('40 12/1 30'),
        sh_value('50 12/1 80'),
        sh_value('7 12/1 7'),
        sh_value('mf 12/1 f'),
        tgen
    )
    print(ns)
    
