import numula_path
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *

def test():
    ns = Score();
    ns.ornament(
        '[10]',
        [59, 60, 62],
        2,
        False,
        1/8, 1/4,
        []
    )
    print(ns)

#test()

def test2():
    ns = sh_score('b orn[0(10) b c 1/16 reps=2 tag=foo] d')
    print(ns)

test2()
