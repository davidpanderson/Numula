import random, math

from numula.nuance import *

def surf():
    s = Score()
    for i in range(1000):
        v = (1-math.cos(i/30.))/2
        v = v*v
        v = .2+.8*v
        n = Note(i/40., .2, random.randint(20, 40), v)
        s.insert_note(n)
    return s
