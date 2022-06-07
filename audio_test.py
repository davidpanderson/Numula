# combine signals with panning

from numula_audio import *

def pos_func(t):
    m = t % 16
    return -1 + t/8

def pos_middle(t):
    return 0

def merge_test():
    s = read_wav('pan_test_stereo.wav')
    osig = zero_signal(len(s))
    scale(s, .4)
    pan_signal(s, 44100, .1, pos_func, osig)
    pan_signal(read_wav('nocturne.wav'), 44100, .2, pos_middle, osig)
    write_wav('panned.wav', osig)

#merge_test()

def test():
    s = read_wav('nocturne.wav')
    scale(s, 2.)
    write_wav('foo.wav', s)
    graph('foo.wav', 4000)

#test()

def file_reader(fname):
    f = open(fname)
    return lambda x: float(f.readline())

def test_pan():
    f = file_reader('pan_test.txt')
    for i in range(10):
        print(f(0))
    #s = read_wav('pan_test.wav')
    #pan_signal(s, 44100, .1,
test_pan()
