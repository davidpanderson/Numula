from notate import *
from note import *
from nuance import *

def test1():
    ns = NoteSet()
    ns.insert_ns(0, n('c d e [f a c] g a b c'))
    ns.done()
    ns.tempo_adjust_pft([linear(60, 120, 8/4)])
    ns.pause_before(3/4, .7)
    ns.roll(3/4, [-.2, -.1, 0], True, True)
    ns.print()
    ns.write_midi('test1.midi')

def test2():
    ns = NoteSet()
    ns.insert_ns(0, n('c d e (foo [f a c] g foo) a b c'))
    ns.insert_measure(Measure(0, 4/4, '4/4'))
    ns.insert_measure(Measure(1, 4/4, '4/4'))
    ns.done()
    ns.t_adjust_list([.1, .2], lambda x: 'foo' in x.tags)
    ns.t_random_uniform(-.1, .1)
    ns.t_random_normal(.1, 3)
    ns.print()
    ns.write_midi('test2.midi')

test1()
test2()
    
