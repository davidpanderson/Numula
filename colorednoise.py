from midiutil import MIDIFile
import colorednoise as cn

# 1/f noise
# see https://github.com/felixpatzelt/colorednoise

def cn_test():
    beta = 1
    samples = 100
    y = cn.powerlaw_psd_gaussian(beta, samples)
    f = MIDIFile(1)
    f.addTempo(0, 0, 120)
    pitch = 48
    dur = 1
    vol = 60
    time = 0
    for i in range(samples):
        pitch = 60+12*y[i]
        f.addNote(0, 0, int(pitch), time, dur, vol)
        print(pitch, y[i])
        time += 1
    with open("colored_noise.midi", "wb") as file:
        f.writeFile(file)
        
cn_test()
