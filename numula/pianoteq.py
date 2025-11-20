# play (or render to .WAV) a MIDI file using Pianoteq
# see https://github.com/davidpanderson/Numula/wiki/Pianoteq

import platform, subprocess, os

# return path of latest PianoTeq executable
#
def pianoteq_path(version):
    s = platform.system()
    if version:
        versions = [version]
    else:
        versions = (9, 8, 7)
    for v in versions:
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

# play MIDI file, launching a new Pianoteq
def play_midi_file(file, preset=None, version=None):
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s" --play --midi %s%s'%(pianoteq_path(version), file, p)
    subprocess.call(cmd, shell=True)

# play MIDI file via RPC
def play_midi_file_rpc(file, preset=None):
    if preset:
        x = preset.split('/')
        if len(x) == 1:
            loadPreset(x[0], '')
        else:
            loadPreset(x[1], x[0])
    loadMidiFile(file)
    midiPlay()

# play score, launching a new Pianoteq
def play_score_aux(ns, preset=None):
    ns.write_midi('data/temp.midi')
    play_midi_file('data/temp.midi', preset)

# play score using RPC to Pianoteq server
def play_score(ns, preset=None):
    ns.write_midi('data/temp.midi')
    play_midi_file_rpc('data/temp.midi', preset)

# render MIDI file to .WAV
def midi_to_wav(ifile, ofile, mono=False, preset=None, version=None):
    m = ' --mono' if mono else ''
    p = ' --preset "%s"'%preset if preset else ''
    cmd = '"%s"%s --wav %s --headless --midi %s%s'%(pianoteq_path(version), m, ofile, ifile, p)
    print(cmd)
    subprocess.call(cmd, shell=True)

####################  API for remote control of Pianoteq

import sys, requests, json

remote_server = '127.0.0.1:8081'

# run pianoteq as an RPC server
def run_server(version=None):
    cmd = '"%s" --serve 8081'%(pianoteq_path(version))
    subprocess.Popen(cmd, shell=True)

# perform a jsonrpc call and return its result,
# or None if the server is not found.
# according to json-rpc spec, params can be either positional parameters,
# supplied as a list of values
# or they can be sent as a dictionary of values
def rpc(method, params=None, id=0):
    if params is None:
        params=[]
    url = f'http://{remote_server}/jsonrpc'
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": id}

    try:
        result = requests.post(url, json=payload)
    except requests.exceptions.ConnectionError:
        raise Exception(
            'Can\'t connect to Pianoteq.  Run pianoteq_server.py to create server.'
        )
        return None
    r = result.json()
    if 'error' in r:
        raise Exception(r['error']['message'])

def loadMidiFile(file):
    path = os.path.abspath(file)
    return rpc('loadMidiFile', [path])

def midiPlay():
    return rpc('midiPlay')

def midiSeek(t):
    return rpc('midiSeek', [t])

def midiStop():
    return rpc('midiStop')

def midiPause():
    return rpc('midiPause')

def loadPreset(name, bank):
    return rpc('loadPreset', [name, bank])
