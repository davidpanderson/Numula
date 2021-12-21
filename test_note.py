from notate import *
from note import *

def test1():
    ns = NoteSet()
    ns.add_list(0, n('c d e f g a b c'))
    ns.add_pedal(Pedal(4/4, 3/4, True))
    ns.done()
    ns.write_midi('test1.midi')

test1()
        
