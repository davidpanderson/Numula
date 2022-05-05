import note,  notate, pianoteq
from nuance import *

lh = notate.n('1/8 --b- +f +d- b- +f -f -b- +f +d- b- +f -f \
    -b- +f +d- b- +f -f -b- +f +e- -a +f -f \
    -b- +f +d- b- +f -f \
', ['lh'])

rh = notate.n('2/4 ++d- 1/4 b- 3/44 +b- c d- -a b- a g+ a c b- g- \
    f g- e f b- a a- g g- f e e- d d- c d- c b c f e e- \
    2/4 d- 1/4 b-\
', ['rh'])

def main():
    ns = note.NoteSet([rh,lh])
    ns.done()  # need this for sort
    for i in range(5):
        ns.sustain(i*3/4, (i+1)*3/4, lambda n: 'lh' in n.tags)
        ns.vol_adjust_pft(
            [linear(.3, .8, 2/4), linear(.8, .3, 1/4)],
            i*3/4,
            lambda n: 'lh' in n.tags
        )
    ns.done()  # need this for overlap
    
    ns.tempo_adjust_pft(
        [
            linear(90, 110, 8/4),
            linear(110, 80, 7/4)
        ]
    )
    ns.tempo_adjust_pft(
        [
            linear(40, 50, 4/4),
            linear(50, 30, 5/4),
        ], 3/4, normalize=True, pred=lambda n: 'rh' in n.tags
    )

    ns.print()
    ns.write_midi('nocturne.midi')
    pianoteq.play('nocturne.midi')

main()
