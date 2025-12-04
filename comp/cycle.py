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
        print(t, p)
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
#        for i in range(3):
#            yield 1/24

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
    #numula.pianoteq.play_score(ns)
    
#test_cycle()


# Generator for pitches
def cycle_gen(
    bottom: PFT,
    top: PFT,
    incr: PFT
):
    dur = pft_dur(bottom)
    if pft_dur(top) != dur or pft_dur(incr) != dur:
        raise Exception('Inconsistent PFT durations')
    bottom = PFTValue(bottom)
    top = PFTValue(top)
    incr = PFTValue(incr)

    t = yield None
    val = None
    while True:
        if t > dur + epsilon:
            yield None
        if val is None:
            val = bottom.value(0)
            t = yield val
        inc = incr.value(t)
        bt = bottom.value(t)
        tp = top.value(t)
        val += inc
        diff = tp - bt
        if val > tp:
            while val - diff > bt:
                val -= diff
        t = yield val

def test_cycle_gen():
    bottom = sh_vol('45 12/1 40')
    top = sh_vol('55 12/1 80')
    incr = sh_vol('7 12/1 31')
    cg = cycle_gen(bottom, top, incr)
    t = 0
    next(cg)
    while True:
        x = cg.send(t)
        if x is None:
            break;
        print(t, x)
        t += 1/32
#test_cycle_gen()

from typing import Generator

# general function for combining sources of pitch, duration, and volume
# and producing a Score.
# Pitch and duration come from Generators.
# Volume can come from a Generator or a PFT.
#
def player(
    pitch_gen: Generator[int, None, None],
    note_dur: Generator[float, None, None],
    vol: Generator[float, None, None]|PFT,
    duration: float,
    play: Callable
) -> Score:
    ns = Score()
    t = 0
    vol_is_pft = False
    next(pitch_gen)
    print(type(vol))
    if isinstance(vol, list):
        vpft = PFTValue(vol)
        vol_is_pft = True
    while t <= duration:
        p = pitch_gen.send(t)
        d = next(note_dur)
        if vol_is_pft:
            v = vpft.value(t)
        else:
            v = next(vol)
        play(ns, t, p, d, v/2)
        t += d
    return ns

def dur_gen():
    while True:
        yield 1/32

def play_note(ns, t, p, d, v):
    ns.insert_note(Note(t, d, int(p), v))
    
def test_player():
    bottom = sh_vol('45 12/1 40')
    top = sh_vol('55 12/1 80')
    incr = sh_vol('7 12/1 31')
    cg = cycle_gen(bottom, top, incr)
    ns = player(
        cg,
        dur_gen(),
        sh_vol('pp 6/1 ff 6/1 pp'),
        12/1,
        play_note
    )
    #print(ns)
    numula.pianoteq.play_score(ns)

test_player()
