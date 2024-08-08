# play (or render to .WAV) a MIDI file using Pianoteq
# see https://github.com/davidpanderson/Numula/wiki/Pianoteq

import platform, subprocess, os

# return path of latest PianoTeq executable
#
def pianoteq_path():
    s = platform.system()
    for v in (8, 7):
        if s == 'Windows':
            p = 'c:/program files/modartt/pianoteq %d/pianoteq %d.exe'%(v,v)
        elif s == 'Darwin':
            p = '/Applications/Pianoteq %d/Pianoteq %d.app/Contents/MacOS/Pianoteq %d'%(v,v,v)
        elif s == 'Linux':
            p = './Pianoteq %d/amd64/Pianoteq %d'%(v,v)
        else:
            raise Exception("OS not supported")
        if os.path.isfile(p):
            return p
    raise Exception('Pianoteq not found')
    
def play(file, preset=None):
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s" --play --midi %s%s'%(pianoteq_path(), file, p)
    subprocess.call(cmd, shell=True)

def play_score(ns):
    # TODO: use tempfile
    ns.write_midi('data/temp.midi')
    play('data/temp.midi')

def midi_to_wav(ifile, ofile, mono=False, preset=None):
    m = ' --mono' if mono else ''
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s"%s --wav %s --headless --midi %s%s'%(pianoteq_path(), m, ofile, ifile, p)
    print(cmd)
    subprocess.call(cmd, shell=True)
