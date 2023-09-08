http://localhost:8081/jsonrpc
----------------
Pianoteq v8.0.0/20221117 JSON-RPC API Reference

getInfo()

Return various informations about the current state of Pianoteq.


getPerfInfo()

Return cpu performance informations.


quit()

Immediately quit Pianoteq.


randomizeParameters(amount=1.0)

Randomize the value of parameters, just like the 'Random' button in the interface.


getListOfPresets(preset_type="full")

Return the list of presets. preset_type can have the following values: {}.


activate(serial,device_name)


getActivationInfo()

Get activation info.


loadPreset(name, bank="", preset_type="full")

Load the specified preset. preset_type can have the following values: full, equ, vel, mic, reverb, tuning, effect_rack, effect1, effect2, effect3.


savePreset(name, bank, preset_type="full")

Save the current preset.


deletePreset(name, bank, preset_type="full")

Delete the current preset (remove its file on disk).


resetPreset()

Reset parameters to saved preset.


nextPreset()


prevPreset()


nextInstrument()


prevInstrument()


abSwitch()

Switch A and B presets.


abCopy()

Copy current (A or B) preset to the other one (B or A).


undo()

Undo last edition.


redo()

Redo last edition.


getParameters()

Return the list of parameters, with their respective values.


setParameters(list=[])

Change the value for the list of parameters provided. The list uses the same format as the list returned by getParameters, except that many fields can be omitted. The requirement is just to supply 'id' to identify the parameter, and either 'normalized_value' or 'text' to specify its new value.


loadMidiFile(path)

Load the specified MIDI file. If the argument is the name of a folder, or a list of strings, then a playlist will be loaded.


saveMidiFile(path)

Save the currently loaded MIDI file.


midiSend(bytes=[])

send raw MIDI bytes to the engine.


getMetronome()

Return the metronome state.


setMetronome(enabled=null, bpm=null, volume_db=null, timesig=null, accentuate=null)

Change the metronome state.


loadFile(path)

Load any supported file (fxp/mfxp/scl/kbm/ptq/wav..


getSequencerInfo()

Return the MIDI sequencer state.


midiPlay()

Play MIDI sequence.


midiStop()

Stop MIDI sequence.


midiPause()

Pause MIDI sequence.


midiRewind()

Rewind MIDI sequence.


midiRecord()

Record MIDI sequence.


midiSeek(seconds)

Change position in MIDI sequence.


panic()

Reset all MIDI state.


getAudioDeviceInfo()

Return information of the current audio device selected.


getListOfAudioDevices()

Return the list of audio devices available.


list()

Get the list of jsonrpc functions.


Usage example (python)
#!/usr/bin/env python3

'''Simple example of use of the JSON-RPC api of Pianoteq. For more info about JSON-RPC, see https://www.jsonrpc.org/specification
'''

import os, sys
import argparse
import requests
import json

remote_server = 'localhost:8081'

# perform a jsonrpc call and return its result, or None if the server is not found.
# according to json-rpc spec, params can be either positional parameters, supplied as a list of values
# or they can be sent as a dictionnary of values
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
        print('Connection error..')
        return None

    return result.json()


# perform a jsonrpc call, the function and arguments are in the 's' string. Arguments must be in json form
# so for example the following call is valid:
#    rpcFromString('loadPreset({"name":"YC5 Pop"})')  # arguments sent as dictionnary of value
#  or:
#    rpcFromString('loadPreset(["YC5 Pop"])')         # arguments set as list of parameter values
# (requiring json syntax is not very convenient, but it does not require custom parsing code)
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

# read-eval-print loop, requires the 'readline' python module
def repl():
    import readline

    # command history is loaded/saved in a file
    histfile = os.path.expanduser('~/.config/modartt_jsonrpc.history')
    if not os.path.exists(histfile):
        os.makedirs(os.path.dirname(histfile), exist_ok=True)
        open(histfile, "w").close()
    readline.read_history_file(histfile)

    # allow completion of partial function names by pressing the TAB key
    def make_completer(words):
        def custom_complete(text, state):
            results = [x for x in words if x.startswith(text)] + [None]
            return results[state] + " "
        return custom_complete

    # retrieve the list of functions from Pianoteq
    words = None
    try:
        r = rpc('list') # this is the jsonrpc function that returned the list of supported functions
        words = { x['name'] for x in r['result'] }
    except:
        pass
    if words is None:
        print('could not fetch the list of functions, completion will be disabled..')

    readline.parse_and_bind('tab: complete')
    readline.set_completer(make_completer(words))

    print('Ctrl-C to exit')

    try:
        while True:
            s = input('ptq >> ').strip()
            if (s == '?' or s == 'help'):
                r = rpc('list')
                if r:
                    for x in r['result']:
                        print('{:30}  {}'.format(x['spec'], x['doc']))
                    print("""
  Examples of commands:
         * Retrieve the list of all presets
                    getListOfPresets
         * Get the list of velocity mini-presets
                    getListOfPresets(["vel"])
         * Load a custom velocity preset from the "My Presets" bank:
                    loadPreset(["my custom veloc preset", "My Presets", "vel"])
         * Enable the metronome and change its time signature
                    setMetronome({"enabled": true, "timesig": "3/4"})
         * Load a MIDI file from disk:
                    loadMidiFile(["path/to/my/midifile.mid"])
         * Send a raw MIDI event (here a note-on for A3, at velocity 100)
                    midiSend([[144, 69, 100]])
                   """)

                else:
                    print('List of functions not available..')
                continue

            r=rpcFromString(s)
            if r:
                print(json.dumps(r, indent=4))

    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')
        readline.write_history_file(histfile)
        sys.exit(0)

def runTest():
    # get the full list of presets
    all_presets = rpc("getListOfPresets")["result"]
    print(json.dumps(all_presets[0:3], indent=4))

    if 0:
        # loop on all presets and load them
        for p in all_presets["result"]:
            print(p["name"])
            rpc("loadPreset", params=[p["name"], p["bank"]])


    rpc("loadPreset", params=["YC5 Basic"])
    rpcFromString('loadPreset({"name":"YC5 Pop"})')
    rpcFromString('loadPreset(["YC5 Pop"])')
    rpc("abCopy")
    param_list = rpc("getParameters")["result"]
    print(json.dumps(param_list[0:3], indent=4))

    if 0:
        # loop on all params and set their value to the max (the preset will sound *very* bad)
        for p in param_list:
            del p["index"]
            p["normalized_value"] = 1.0
        rpc("setParameters", params = { "list" : param_list })

    # change instrument condition value
    rpc("setParameters", params = { "list" : {"id":"Condition","normalized_value":0.2} })

    print(json.dumps(rpc("getParameters")["result"], indent=4))
    print(json.dumps(rpc("getInfo")["result"], indent=4))
    print(json.dumps(rpc("getAudioDeviceInfo")["result"], indent=4))



def main(parser):
    global remote_server

    args = parser.parse_args()
    if args.server:
        remote_server = args.server
    if args.run:

        r = rpcFromString(args.run)
        if r is not None:
            print(json.dumps(r, indent=4))
            return 0
        else:
            return 1
    elif args.repl:
        repl()
        return 0
    elif args.test:
        runTest()
        return 0

    parser.print_help(sys.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--server", metavar='IP:PORT', help='specify the server address (default: ' + remote_server + ')')
    parser.add_argument("--test", action='store_true', help='perform a simple test of the api')
    parser.add_argument("--repl", action='store_true', help='start an interactive session, where one can type commands with keyboard')
    parser.add_argument("--run", metavar='command', help='perform the jsonrpc command, for example: \'getListOfPresets()"\' or \'loadPreset([\"YC5 Basic\"])\'')
    sys.exit(main(parser))
