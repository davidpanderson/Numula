# dipa: iteractively edit a Numula program's nuance params
#
# You can select the param you want to vary,
# then use the up and down arrows to change its value.
# When you hit the space bar, a selected part the piece is played.
#
# usage: py dipa.py prog
#
# The program (prog.py) must:
# 1) declare adjustable variables with e.g.
#   var('v1', IPA_VOL_MULT, .2)
#   It can refer to this as 'v1'
# 2) define a function main() that returns a Score object
#
# commands:
# :p start dur      set playback start/dur (default 0, 1)
# :i                set current var to the ith one
# :i val            assign value to ith var
# :s                show vars and start/dur
# :w                write var values to prog.vars
# :?                show commands
# space             play from start to start+dur
# up/down arrow     inc/dec current var

import sys, time, os
import readchar
import numula.pianoteq
import numula.pianoteq_rpc
import numula.ipa as ipa

def show_commands():
    print('''
commands:
:p start dur      set playback start/dur (default 0, 1)
:i                set current var to the ith one
:i val            assign value to ith var
:s                show vars and start/dur
:w                write var values to prog.vars
:?                show commands
space             play from start to start+dur
up/down arrow     inc/dec current var
    ''')

def type_name(type):
    if type == IPA_VOL: return 'Volume'
    if type == IPA_VOL_MULT: return 'Volume multiplier'
    if type == IPA_DT_SCORE: return 'Score time'
    if type == IPA_DT_SEC: return 'Seconds'
    if type == IPA_TEMPO: return 'Tempo'
    if type == IPA_BOOL: return ''
    return '???'

# show non-hidden variables and other info
#
def show(cur_var, start, dur):
    print('variables:')
    n = len(ipa.vars)
    for i in range(n):
        x = ipa.vars[i]
        name = x['name']
        t = ''
        if x['tags']:
            if not ipa.tags_set(x['tags']):
                continue
            t = ' (tags: %s)'%(', '.join(x['tags']))
        d = ' desc %s'%(x['desc']) if x['desc'] else ''
        if ipa.numeric(x['type']):
            print('%d. %10s: %.2f %s%s%s'%(
                i+1, name, ipa.get(name), type_name(x['type']), t, d
            ))
        else:
            print('%d. %s: %s %s%s%s'%(
                i+1, name, ipa.get(name), type_name(x['type']), t, d
            ))

    print('current var: %d'%(cur_var+1))
    print('start time: %f duration: %f'%(start, dur))

# write adjustable variables to a file
#
def write_vars(fname):
    with open(fname, 'w') as f:
        for var in ipa.vars:
            name = var['name']
            if ipa.numeric(var['type']):
                f.write('%s %f\n'%(name, ipa.get(name)))
            else:
                f.write('%s %s\n'%(name, ipa.get(name)))

# inc or dec a numeric adjustable variable
#
def adjust(ivar, up):
    x = ipa.vars[ivar]
    if not ipa.numeric(x['type']):
        print(x['name']+' is not numeric')
        return
    name = x['name']
    val = ipa.get(name)
    if up:
        val += x['step']
        if val > x['hi']:
            val = x['hi']
    else:
        val -= x['step']
        if val < x['lo']:
            val = x['lo']
    ipa.set(name, val)
    print('%s: %f'%(name ,val))

def ipa_main():
    global ns
    global __name__
    __name__ = 'foo'
    if len(sys.argv) != 2:
        raise Exception('usage: dipa prog')
    prog = sys.argv[1]
    prog_vars = ipa.vars_file_path(prog)
    prog_midi = 'data/%s.midi'%(prog)

    # run the program to get its adjustable variables
    #
    with open(prog+'.py') as f:
        prog_source = f.read()
    exec(prog_source, globals())
    ns = main()
    try:
        ipa.vars
    except:
        raise Exception('no adjustable vars')
    cur_var = 0

    if os.path.exists(prog_vars):
        print('reading vars from ', prog_vars)
        ipa.read_vars(prog)

    start = 0
    dur = 1
    show(cur_var, start, dur)

    dirty = True
        # true if variables have changed;
        # we need to regenerate score on next play
    while True:
        x = readchar.readkey()
        if x == ':':
            line = input(':')
            if not line:
                continue
            words = line.split()

            # select current var, or set var value
            if words[0].isnumeric():
                j = int(words[0]) - 1
                if j<0 or j >= len(ipa.vars):
                    print('invalid variable number')
                    continue
                v = ipa.vars[j]
                if ipa.numeric(v['type']):
                    cur_var = j
                    if len(words) > 1:
                        try:
                            val = float(words[1])
                            ipa.set(v['name'], val)
                        except:
                            print('bad value ', words[1])
                            continue
                        dirty = True
                    else:
                        print('%s: %f'%(v['name'], ipa.get(v['name'])))
                else:
                    if len(words) < 2:
                        print('must supply a value')
                        continue
                    if v['type'] == IPA_BOOL:
                        if words[1] == 't':
                            ipa.set(v['name'], True)
                        elif words[1] == 'f':
                            ipa.set(v['name'], False)
                        else:
                            print('bad value: use t/f')
                            continue
                    else:
                        ipa.set(v['name'], words[1])
                    dirty = True

            # show commands
            elif words[0] == 's':
                show(cur_var, start, dur)

            # set start/end times
            elif words[0] == 'p':
                x = cmd.split()
                if len(words) != 3:
                    print('usage: :t start dur')
                    continue
                start = float(words[1])
                dur = float(words[2])
                dirty = True

            # write vars to disk
            elif words[0] == 'w':
                write_vars(prog_vars)

            elif words[0] == 'q':
                if dirty:
                    print('There are unsaved changes.')
                    print(':w to save; ^C to quit without saving.')
                else:
                    break

            elif words[0] == '?':
                show_commands()

            else:
                print('unrecognized command: %s'%line)
        elif x == readchar.key.UP:
            adjust(cur_var, True)
            dirty = True
        elif x == readchar.key.DOWN:
            adjust(cur_var, False)
            dirty = True
        elif x == ' ':
            if dirty:
                print('computing score')
                exec(prog_source, globals())
                ns = main()
                #print(ns)
                #print(start, dur)
                ns.trim(start, start+dur)
                ns.write_midi(prog_midi)
                numula.pianoteq_rpc.loadMidiFile(prog_midi)
                dirty = False
            numula.pianoteq_rpc.midiSeek(0)
            numula.pianoteq_rpc.midiPlay()

ipa_main()
