# This file is part of Numula
# Copyright (C) 2022 David P. Anderson
#
# Numula is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Numula is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Numula.  If not, see <http://www.gnu.org/licenses/>.

# example of using tempo_adjust_pft() for rubato.
# a few measures from Chopin's Nocturne no 1

import note,  notate, pianoteq
from nuance import *

lh = notate.n('1/8 --b- +f +d- b- +f -f -b- +f +d- b- +f -f \
    -b- +f +d- b- +f -f -b- +f +e- -a +f -f \
    -b- +f +d- b- +f -f \
', ['lh'])

rh = notate.n('2/4 ++d- 1/4 b- 3/44 +b- c d- -a b- a g+ a c b- g- \
    f g- e f b- (port a a- g g- f e e- d d- c d- c b port) c f e e- \
    2/4 d- 1/4 b-\
', ['rh'])

def main():
    ns = note.NoteSet([lh, rh])

    for i in range(5):
        ns.sustain(i*3/4, (i+1)*3/4, lambda n: 'lh' in n.tags)
        
    ns.done()
    
    for i in range(5):
        ns.vol_adjust_pft(
            [linear(.3, .8, 2/4), linear(.8, .3, 1/4)],
            i*3/4,
            lambda n: 'lh' in n.tags
        )

    ns.tempo_adjust_pft(
        [
            linear(90, 110, 8/4),
            linear(110, 80, 7/4)
        ]
    )

    # timing in RH
    ns.tempo_adjust_pft(
        [
            linear(40, 50, 2/4),
            linear(50, 35, 2/4),
            delta(.15),
            linear(30, 50, 3/4),
            linear(50, 30, 2/4),
            delta(.3, False)
        ], 3/4, normalize=True, pred=lambda n: 'rh' in n.tags
    )

    # portamento in RH
    ns.perf_dur_rel(.5, lambda n: 'port' in n.tags)

    ns.print()
    ns.write_midi('data/nocturne.midi')
    pianoteq.play('data/nocturne.midi')

main()
