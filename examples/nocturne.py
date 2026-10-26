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

import numula_path
from numula.notate_score import *
from numula.nuance import *
from numula.notate_nuance import *
import numula.pianoteq as pianoteq

lh = sh_score('1/8 --b- +f +d- b- +f -f -b- +f +d- b- +f -f \
    -b- +f +d- b- +f -f -b- +f +e- -a +f -f \
    -b- +f +d- b- +f -f \
').tag('lh')

rh = sh_score('2/4 ++d- 1/4 b- 3/44 +b- c d- -a b- a g+ a c b- g- \
    f g- e f b- (port a a- g g- f e e- d d- c d- c b port) c f e e- \
    2/4 d- 1/4 b-\
').tag('rh')

def main():
    nuance = True
    make_wav = False
    preset = 'HB Steinway D Classical Recording'

    if nuance:
        ns = Score()
        lh.vsustain_pft(
            sh_pedal('*5 (3/4) *')
        )
    else:
        ns = Score(tempo=90)
        
    ns.append_scores([lh, rh])

    if nuance:
        ns.vol_adjust_pft(
            sh_vol('*5 pp 2/4 p 1/4 pp *'), 0,
            lambda n: 'lh' in n.tags
        )
        ns.vol_adjust_pft(
            sh_vol('mf 3/4 pp [ mp 3/8 mf 3/8 mp 6/8 mf 6/8 p [ mp 3/4 pp'), 0,
            lambda n: 'rh' in n.tags
        )

        ns.tempo_adjust_pft(
            sh_tempo('*4 80 3/8 90 3/8 80 .05p * 80 3/8 90 3/8 40')
        )
        # timing in RH

        ns.tempo_adjust_pft(
            sh_tempo('60 3/4 40'),
            3/4, normalize=True, selector=lambda n: 'rh' in n.tags
        )
        ns.tempo_adjust_pft(
            sh_tempo('40 3/4 80 3/4 40'),
            6/4, normalize=True, selector=lambda n: 'rh' in n.tags
        )

        # portamento in RH
        ns.adjust_dur_rel(.6, lambda n: 'port' in n.tags)
    #print(ns)

    if make_wav:
        fname = if do_nuance 'nocturne' else 'nocturne_plain'
        ns.write_midi(f'data/{fname}.midi')
        numula.pianoteq.midi_to_wav(
            f'data/{fname}.midi',
            f'data/{fname}.wav',
            preset=preset
        )
    else:
        numula.pianoteq.play_score(ns, preset)

main()
