import random

from numula.nuance import *

def surf():
    s = Score()
    for i in range(1000):
        n = Note(i/10., 1, random.randint(20, 40), .5)
        s.insert_note(n)
    return s
