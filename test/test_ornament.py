import numula_path
from numula.nuance import *

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

test()
