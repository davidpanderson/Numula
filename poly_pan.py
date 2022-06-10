# demo of spatialized polyphony
# Three voices, each with the same tempo adjustment,
# are written to separate mono files,
# the combined with independent panning

import math
from note import *
from nuance import *
import numula_audio, pianoteq

def main():
    ns = NoteSet()
    for i in range(32):
        ns.insert_note(Note(i*2/32, 2/32, 60, .5, ['v0']))
    for i in range(25):
        ns.insert_note(Note(i*2/25, 2/25, 68, .5, ['v1']))
    for i in range(37):
        ns.insert_note(Note(i*2/37, 2/37, 74, .5, ['v2']))
    ns.done()
    ns.tempo_adjust_pft(
        [
            linear(60, 80, 4/4),
            linear(80, 60, 4/4)
        ]
    )

    # panning pattern:
    # 0 1 2
    # 2 0 1
    # 1 2 0
    pos_pft = [
        [
            linear(-1, 0, 4/4),
            linear(0, 1, 4/4)
        ],
        [
            linear(0, 1, 4/4),
            linear(1, -1, 4/4)
        ],
        [
            linear(1, -1, 4/4),
            linear(-1, 0, 4/4)
        ]
    ]

    # make MIDI and WAV files for each of the voices,
    # and get the max length.
    max_nframes = 0
    for i in range(3):
        ns.write_midi('data/v%d.mid'%i, lambda n: 'v%d'%i in n.tags)
        pianoteq.midi_to_wav('data/v%d.mid'%i, 'data/v%d.wav'%i)
        nf = numula_audio.nframes('data/v%d.wav'%i)
        if nf > max_nframes:
            max_nframes = nf

    # allocate a signal buffer, and copy the 3 voices into it,
    # panning according to the above PFTs
    signal = numula_audio.zero_signal_ns(max_nframes*2)
    for i in range(3):
        numula_audio.pan_signal(
            numula_audio.read_wav('data/v%d.wav'%i),
            44100, .1,
            ns.get_pos_array(pos_pft[i], 44100),
            signal
        )

    # write signal buffer to WAV file
    numula_audio.write_wav('data/pan_test.wav', signal)

main()
