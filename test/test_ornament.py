import numula_path
from numula.ornament import *

def test():
    ns = ScoreOrnament();
    ns.ornament(
        '[10]',
        [59, 60, 62],
        2,
        False,
        1/8, 1/4,
        []
    )
    print(ns)

test()
