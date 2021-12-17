from notate import *
from nuance import *

def test1():
    ns = NoteSet()
    ns.add_list(0, n('c d e [f a c] g a b c'))
    timing_init(ns)
    #tempo_seg(ns, 8/4, linear, [60,120])
    #pause(ns, 3/4, .7, False)
    roll(ns, 3/4, [-.2, -.1, 0], True, True)
    ns.print()
    ns.write_midi('test1.midi')

test1()
