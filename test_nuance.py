from notate import *
from nuance import *

def test1():
    ns = NoteSet()
    ns.add_list(0, n('c d e [f a c] g a b c'))
    ns.done()
    #tempo_seg(ns, 8/4, linear, [60,120])
    #pause(ns, 3/4, .7, False)
    roll(ns, 3/4, [-.2, -.1, 0], True, True)
    ns.print()
    ns.write_midi('test1.midi')

def test2():
    ns = NoteSet()
    ns.insert_ns(0, n('c d e (foo [f a c] g foo) a b c'))
    ns.insert_measure(Measure(0, 4/4, '4/4'))
    ns.insert_measure(Measure(1, 4/4, '4/4'))
    ns.done()
    t_adjust_list(ns, [.1, .2], lambda x: 'foo' in x.tags)
    #t_random_uniform(ns, -.1, .1)
    t_random_normal(ns, .1, 3)
    ns.print()
    ns.write_midi('test2.midi')
    
test2()
    
