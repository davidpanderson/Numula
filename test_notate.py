from note import *
from notate import *

def test1():
    s = 'c (foo d 1/8 _ e foo)'
    ns = NoteSet()
    ns.append_ns([n(s)])
    ns.done()
    ns.print()
    ns.write_midi('test1.midi')

test1()
