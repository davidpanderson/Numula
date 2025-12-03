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
    
#test_cycle()

from abc import ABC, abstractmethod

# an object that encapsulates a function of time
class Function_of_Time(ABC):
    @abstractmethod
    def value(t):
        pass

class CycleGen(Function_of_Time):
    def __init__(
        bottom: PFT,
        top: PFT,
        incr: PFT
    ):
        self.bottom = PFTValue(bottom)
        self.top = PFTValue(top)
        self.incr = PFTValue(incr)
        self.val = None;    # last returned value
        self.dur = pft_dur(bottom)
        if pft_dur(top) != self.dur or pft_dur(incr) != self.dur
            raise Exception('Inconsistent PFT durations')

    def value(t):
        if t > dur + epsilon:
            return None
        if self.val is None:
            self.val = bottom.value(t)
            return self.val
        inc = incr.value(t)
        bt = bottom.value(t)
        tp = top.value(t)
        self.val += inc
        diff = tp - bt
        if self.val > top.value(t):
            while self.val-diff > bt:
                self.val -= diff
        return self.val

def test_cycle_gen():
    bottom = sh_vol('45 12/1 40')
    top = sh_vol('55 12/1 80')
    incr = sh_vol('7 12/1 31')
    cg = CycleGen(bottom, top, incr)
    t = 0
    while True:
        x = cg.value(t)
        if x is None:
            break;
        print(t, x)
        t += 1/4
    
def player(
    pitch_gen: Function_of_Time,
    dur: generator,
    vol: generator|PFT,
    play: function
)->Score:
    pass
