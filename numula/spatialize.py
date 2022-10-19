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


# code to:
# - read .wav files into signals (arrays of float samples)
# - manipulate and combine signals (e.g. scale, pan)
# - write signals as .wav files
# - play .wav files using
# see https://github.com/davidpanderson/Numula/wiki/spatialize.py

# see https://docs.python.org/3/library/wave.html

import wave, struct, math, subprocess, platform
import matplotlib.pyplot as plot

# print params of a .wav file
def show_info(fname):
    obj = wave.open(fname)
    print( "Number of channels",obj.getnchannels())
    print ( "Sample width",obj.getsampwidth())
    print ( "Frame rate.",obj.getframerate())
    print ("Number of frames",obj.getnframes())
    print ( "parameters:",obj.getparams())
    obj.close()

def nframes(fname):
    obj = wave.open(fname)
    return obj.getnframes()

# draw a graph of the first N frames of a .wav file
def graph_wav(fname, nframes):
    obj = wave.open(fname)
    x = obj.readframes(nframes)
    obj.close()
    #print(len(x))
    y = struct.unpack("%dh"%(nframes*2), x)
    y1 = [0]*nframes
    y2 = [0]*nframes
    for i in range(nframes):
        y1[i] = y[i*2]
        y2[i] = y[i*2+1]
    plot.rcParams['figure.figsize'] = (12,8)
    plot.plot(range(nframes), y1, label='L')
    plot.plot(range(nframes), y2, label='R')
    plot.show()

# graph a position array
def graph_pos(pos_array):
    nframes = len(pos_array)
    plot.rcParams['figure.figsize'] = (12,8)
    plot.plot(range(nframes), pos_array)
    plot.show()
    
# read .wav file as array of floats
def read_wav(fname):
    f = wave.open(fname)
    nsamples = f.getnframes()*2
    samples = [0.]*nsamples
    buf_frames = 10000
    ns = 0
    while True:
        x = f.readframes(buf_frames)
        nbytes = len(x)
        if nbytes == 0: break
        buf_nsamples = nbytes//2
        s = struct.unpack("%dh"%(buf_nsamples), x)
        for i in range(buf_nsamples):
            a = float(s[i])
            samples[ns] = a
            ns += 1
    print('read',nsamples//2,'frames from', fname)
    return samples      

# write array of floats as .wav file
def write_wav(fname, samples):
    f = wave.open(fname, 'wb')
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(44100)
    buf_nsamples = 10000
    nsamples = len(samples)
    nwritten = 0
    while nwritten < nsamples:
        ns = buf_nsamples
        if nwritten + ns > nsamples:
            ns = nsamples-nwritten
        isamples = [0]*ns
        for i in range(ns):
            isamples[i] = int(samples[nwritten+i])
        x = struct.pack("%dh"%(ns), *isamples)
        f.writeframes(x)
        nwritten += ns
    print('wrote',nsamples//2,'frames to',fname)

# create a zero signal of given length
def zero_signal_t(dur, framerate):
    nsamples = math.ceil(2*dur*framerate)
    return [0]*nsamples

def zero_signal_ns(nsamples):
    return [0]*nsamples

# scale signal
def scale(samples, gain):
    for i in range(len(samples)):
        samples[i] *= gain
        
# add the input signal "isig" to the output signal "osig",
# panning it according to the array pos: 0..1
# "ang" is the separation (0..1) between the input chans.
# if 0, the channels are summed (mono)
def pan_signal(isig, framerate, ang, pos_array, osig):
    inframes = len(isig)//2
    pnframes = len(pos_array)
    print('pan_signal; input %d frames, pos_array %d frames'%(inframes, pnframes))
    for i in range(inframes):
        a = isig[i*2]
        b = isig[i*2+1]
        if i < pnframes:
            p = pos_array[i]
        else:
            p = pos_array[pnframes-1]
        if ang == 0:
            avg = (a+b)/2
            pp = p*math.pi/2
            osig[i*2] += avg*math.cos(pp)
            osig[i*2+1] += avg*math.sin(pp)
        else:
            p0 = max(p-ang, 0)*math.pi/2
            p1 = min(p+ang, 1)*math.pi/2
            osig[i*2] += a*math.cos(p0)
            osig[i*2+1] += a*math.sin(p0)
            osig[i*2] += b*math.cos(p1)
            osig[i*2+1] += b*math.sin(p1)

def play_wav(fname):
    s = platform.system()
    if s == 'Windows':
        prog = "C:\Program Files (x86)\Windows Media Player/wmplayer.exe"
        cmd = '"%s" %%cd%%/%s'%(prog, fname)
            # wmplayer requires full path
    else:
        raise Exception("OS not supported")

    print(cmd)
    subprocess.call(cmd, shell=True)

play_wav("data/pan_test.wav")
    
