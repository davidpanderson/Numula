import numula_path
from numula.nuance import *
from numula.notate_score import *
from numula.notate_nuance import *
import numula.pianoteq as pianoteq

def test():
    ns = Score();
    ns.append_ornament(
        [60, 59, 60, 59, 60],
        False,
        1/8, 1/4,
        []
    )
    print(ns)
    #pianoteq.play_score(ns)

#test()

def test2():
    #ns = sh_score('b orn[*2 d c * b c 1/8 tag=foo] d')
    ns = sh_score('g orn[e d 1/8 ] d')
    print(ns)
    #pianoteq.play_score(ns)
#test2()

def test3():
    ns = sh_score('b orn[b *2 c b * c 1/8 tag=foo] d')
    for orn in filter(lambda x: 'foo' in x.tags, ns.ornaments):
        pft = sh_tempo('40 1/1 80')
        pft_scale_dur(pft, orn.orn_dur)
        ns.tempo_adjust_pft(
            pft,
            orn.start_time,
            lambda n: n in orn.notes,
            normalize=True
        )
    print(ns)
    #pianoteq.play_score(ns)
#test3()

def test4():
    ns = sh_score('1/4 orn[c d e c 1/8]')
    print(ns)
#test4()
