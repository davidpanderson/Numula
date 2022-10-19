# demo of spatialized polyphony using Bach's Fugue 18 from WTC II
# Three voices are written to separate .wav files,
# then combined with independent panning

import math
from numula.nscore import *
from numula.notate_score import *
from numula.nuance import *
import numula.spatialize, numula.pianoteq

def main():
    v0 = n('1/8 (theme +g+ a+ b a+ d+ -d+ | g+ b a+ b a+ g+ | a+ b c+ b e -g+ | a+ c+ b c+ b a+ | 1/4 b theme) 1/8 b+ 6/8 c+ \
        3/8 b+ | 1/4 c+ 1/8 c++ 6/8 d+ | 3/8 c++ | 1/8 d+ 3/8 c+ 1/8 a+ b+ | c+ 3/8 b 1/8 g+ a+ \
        4/8 b 1/8 a+ c+ | -f++ +d+ -g+ 4/8 c+ | 1/8 e d+ c+ b a+ | 1/4 b 1/8 d+ 5/8 g+ | 1/8 f++ 1/4 g+ 1/8 b \
        1/4 -c+ 1/8 d+ e d+ c+ | 3/8 d+ c+ | b a+ | 1/8 g+ 7/8 . | 1/8 +d+ 1/4 d+ 1/8 c++ \
        2/8 d+ 6/8 . | 1/8 e 1/4 d+ 1/8 c+ | 1/4 b 1/8 g+ 1/4 a+ 1/8 b+ | 1/8 c+ g+ 1/4 c+ 1/8 a+ b+ | 3/8 e 4/8 d+ \
        1/8 c+ 1/4 +a 1/8 f++ g+ | 6/8 -c+ | b | 5/8 a+ 1/8 c++ | d+ e+ 2/8 f+ 1/8 e+ g+ \
        -c++ e+ -a+ 6/8 d+ | 3/8 c++ | 6/8 d+ ')
    v1 = n('6/8 . . . . (theme 1/8 d+ e+ f+ e+ a+ -a+ \
        d+ f+ e+ f+ e+ d+ | e+ f+ g+ f+ b -d+ | e+ g+ f+ g+ f+ e+ | 1/4 f+ theme) 1/8 f++ 1/4 g+ 1/8 f+ | 1/4 e 1/8 e+ 1/4 f+ 1/8 e \
        d+ g+ -g+ 5/8 c+ | 1/8 b a+ +g+ f++ | 5/8 g+ 1/8 f++ | 2/8 g+ 3/8 . 1/8 b | c+ d+ e d+ c+ 2/8 b \
        1/8 a+ g+ 4/8 f+ | 1/8 f+ 2/8 b 1/8 g+ 2/8 a+ | 1/8 -d+ 2/8 g+ 1/8 e+ f++ | (theme g+ a+ b a+ d+ -d+ | g+ b a+ b a+ g+ \
        a+ b c+ b e -g+ | a+ c+ b c+ b a+ | b theme) -b 2/8 e 1/8 c+ d+ | 3/8 -g+ . | 2/8 . 1/8 ++a 2/8 f+ 1/8 g+ \
        3/8 e d+ | 1/8 e+ f++ g+ 4/8 a+ | 1/8 g+ f+ e+ g+ d+ | c++ d+ e+ 4/8 f+ | 1/8 g+ a+ 6/8 g+ \
        1/8 f+ a+ -d+ | +e+ f+ 2/8 g+ 1/8 a+ e+ | 6/8 f+ ')
    v2 = n('6/8 . . . . . \
        . . . . . \
        . . | (theme 1/8 g+ a+ b a+ d+ -d+ | g+ b a+ b a+ g+ | a+ b c+ b e -g+ \
        a+ c+ b c+ b a+ | 1/4 b theme) 1/8 g+ 1/4 e+ 1/8 f++ | 1/4 g+ 1/8 e 1/4 c+ 1/8 d+ | 1/4 e 1/8 e+ 6/8 f+ | 3/8 e+ \
        1/4 f+ 1/8 f++ 6/8 g+ | 3/8 f++ | g+ f+ | e d+ | 1/8 c+ +g+ 2/8 c+ 1/8 a+ b+ \
        3/8 c+ 4/8 b | 1/8 a+ g+ f++ a+ -d+ | 1/4 g+ 1/8 -g+ 4/8 +g+ | 1/8 f+ e+ d+ f+ -a+ | 1/24 b c+ b c+ b c+ b c+ b c+ b c+ b c+ b 1/16 a+ b \
        6/8 a+ | . d+ ')
    ns = Score()
    ns.insert_score(v0, tag='v0')
    ns.insert_score(v1, tag='v1')
    ns.insert_score(v2, tag='v2')
    
    if True:
        def vol_pft():
            x = []
            for i in range(33):
                x.append(Linear(.3, .4, 3/8))
                x.append(Linear(.4, .3, 3/8))
            return x
        ns.vol_adjust_pft(vol_pft())
        ns.vol_adjust(1.4, lambda n: 'theme' in n.tags)

    if True:

        def tempo_pft():
            x = []
            for i in range(8):
                for j in range(3):
                    x.append(Linear(90, 93, 3/8))
                    x.append(Linear(93, 90, 3/8))
                    x.append(Delta(.015, False))
                x.append(Linear(90, 85, 6/8))
                x.append(Delta(.02, False))
            x.append(Delta(.02, False))
            return x
                    
        ns.tempo_adjust_pft(tempo_pft())
        t_random_normal(ns, .008, 2)
        
    if False:
        ns.write_midi('data/poly_pan.midi')
        pianoteq.play('data/poly_pan.midi')
        return

    # panning pattern:
    pos_pft = [
        [
            Linear(.5, 1, 4*6/8),
            Linear(1, 1, 28*6/8)
        ],
        [
            Linear(.5, .5, 4*6/8),
            Linear(.5, 0, 8*6/8),
            Linear(0, 0, 20*6/8)
        ],
        [
            Linear(.5, .5, 32*6/8)
        ]
    ]

    presets = [
        'NY Steinway Model D',
        'C. Grimaldi Harpsichord A',
        'Pleyel Close Mic'
    ]
        
    # make MIDI and WAV files for each of the voices,
    # and get the max length.
    max_nframes = 0
    for i in range(3):
        ns.write_midi('data/v%d.mid'%i, lambda n: 'v%d'%i in n.tags)
        pianoteq.midi_to_wav('data/v%d.mid'%i, 'data/v%d.wav'%i, preset=presets[i])
        nf = spatialize.nframes('data/v%d.wav'%i)
        if nf > max_nframes:
            max_nframes = nf

    # allocate a signal buffer, and copy the 3 voices into it,
    # panning according to the above PFTs
    signal = spatialize.zero_signal_ns(max_nframes*2)
    for i in range(3):
        pos_array = ns.get_pos_array(pos_pft[i], 44100)
        #spatialize.graph_pos(pos_array)
        spatialize.pan_signal(
            spatialize.read_wav('data/v%d.wav'%i),
            44100, .1,
            pos_array,
            signal
        )

    # write signal buffer to WAV file
    spatialize.write_wav('data/pan_test.wav', signal)

main()
