# API for remote control of Pianoteq

import sys, os, subprocess
import requests
import json
import numula.pianoteq as pianoteq

remote_server = '127.0.0.1:8081'

# run pianoteq as an RPC server
def run_server():
    cmd = '"%s" --serve 8081'%(pianoteq.pianoteq_path())
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
        result=requests.post(url, json=payload)
    except requests.exceptions.ConnectionError:
        print('Connection error.  Run pianoteq_server.py to create server.')
        return None
    #return result
    return result.json()


# perform a jsonrpc call, the function and arguments are in the 's' string.
# Arguments must be in json form
# so for example the following call is valid:
#    rpcFromString('loadPreset({"name":"YC5 Pop"})')
#     arguments sent as dictionary of value
#  or:
#    rpcFromString('loadPreset(["YC5 Pop"])')
#     arguments set as list of parameter values
# (requiring json syntax is not very convenient,
# but it does not require custom parsing code)
def rpcFromString(s):
    params=[]
    s = s.strip()
    l = s.split('(',2)
    fun = s
    args = ''
    if len(l) == 2:
        [fun, args] = l
        if not args.endswith(')'):
            raise Exception('invalid args')
        args=args[:-1]
    if len(args) == 0:
        args = '[]'
    elif not (args.startswith('{') and args.endswith('}')) and not (args.startswith('[') and args.endswith(']')):
        print('Arguments must be either a json dictionary {"name":value, ...} or a json list [value1, value2, ...]')
        return None
    try:
        params=json.loads(args)
    except:
        print(f'Could not parse \'{args}\' as valid json')
        return None

    res=rpc(fun, params)
    return res

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

def loadPreset(name):
    return rpc('loadPreset', [name])
