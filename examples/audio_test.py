# combine signals with panning

from numula.spatialize import *

def pos_func(t):
    m = t % 16
    return -1 + t/8

def pos_middle(t):
    return 0

def merge_test():
    s = read_wav('data/pan_test_stereo.wav')
    osig = zero_signal(len(s))
    scale(s, .4)
    pan_signal(s, 44100, .1, pos_func, osig)
    pan_signal(read_wav('data/nocturne.wav'), 44100, .2, pos_middle, osig)
    write_wav('data/panned.wav', osig)

#merge_test()

def test():
    s = read_wav('data/nocturne.wav')
    scale(s, 2.)
    write_wav('data/foo.wav', s)
    graph_wav('data/foo.wav', 4000)

#test()

def test_pan():
    f = file_reader('data/pan_test.txt')
    for i in range(10):
        print(f(0))
    #s = read_wav('data/pan_test.wav')
    #pan_signal(s, 44100, .1,
test_pan()
