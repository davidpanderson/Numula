# dipa: iteractively edit a Numula program's nuance params
#
# You can select the param you want to vary,
# then use the up and down arrows to change its value.
# When you hit the space bar, it plays a selected part the piece.
#
# usage: dipa prog
#
# The program (prog.py) must:
# 1) declare adjustable variables with
#   nvar(name, val, step, lo=0, hi=1)
#   It can refer to these as 'ipa.name'
#   (ideally it should just be 'name', but I can't figure out how).
# 2) Create a global var 'ns' containing a ScoreBasic
#
# commands:
# :p start dur      set playback start/dur (default 0, 1)
# :v i              set current var to the ith one
# :v i val          assign value to ith var
# :s                show vars, tags, and start/dur
# :t i val          set val of tag i (y/n)
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
:v i              set current var to the ith one
:v i val          assign value to ith var
:s                show vars, tags, and start/dur
:t i val          set val of tag i (y/n)
:w                write var values to prog.vars
:?                show commands
space             play from start to start+dur
up/down arrow     inc/dec current var
    ''')

def show(cur_var, start, dur):
    print('adjustable variables:')
    n = len(ipa.vars)
    for i in range(n):
        x = ipa.vars[i]
        name = x['name']
        t = ''
        if x['tags']:
            if not ipa.tags_set(x['tags']):
                continue;
            t = ' tags: (%s)'%(', '.join(x['tags']))
        d = ' desc %s'%(x['desc']) if x['desc'] else ''
        if ipa.numeric(x['type']):
            print('%d) name: %s value %f step %f%s%s'%(
                i+1, name, ipa.get(name), x['step'], t, d
            ))
        else:
            print('%d) name: %s value %s%s'%(
                i+1, name, ipa.get(name), d
            ))

    n = len(ipa.tags)
    if n:
        print('tags:')
        for i in range(n):
            x = ipa.tags[i]
            name = x['name']
            print('%d) name: %s value:%s'%(
                i+1, name, 'on' if x['value'] else 'off'
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

# inc or dec an numeric adjustable variable
#
def adjust(ivar, up):
    x = ipa.vars[ivar]
    if not ipa.numeric(x['type']):
        printf('not numeric')
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
    prog_vars = prog+'.vars'
    prog_midi = 'data/%s.mid'%(prog)

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
    while True:
        x = readchar.readkey()
        if x == ':':
            cmd = input(':')
            if not cmd:
                continue
            c = cmd[0]

            # set current var, or set var value
            if c == 'v':
                x = cmd.split()
                try:
                    j = int(x[1])
                except:
                    print('invalid variable number')
                    continue
                j -= 1
                if j<0 or j >= len(ipa.vars):
                    print('invalid variable number')
                    continue
                v = ipa.vars[j]
                if ipa.numeric(v['type']):
                    cur_var = j
                else:
                    if len(x) < 3:
                        print('must supply a value')
                        continue
                    ipa.set(v['name'], x[2])

            # set tag value
            elif c == 't':
                x = cmd.split()
                if len(x) != 3:
                    print('syntax: :t i value')
                    continue
                try:
                    j = int(x[1])
                except:
                    print('syntax: :t i value')
                    continue
                if j<=0 or j > len(ipa.tags):
                    print('syntax: :t i value')
                    continue
                if x[2] == 'y':
                    val = True
                elif x[2] == 'n':
                    val = False
                ipa.tags[j-1]['value'] = val

            # show commands
            elif c == 's':
                show(cur_var, start, dur)

            # set start/end times
            elif c == 'p':
                x = cmd.split()
                if len(x) != 3:
                    print('usage: :t start dur')
                    continue
                start = float(x[1])
                dur = float(x[2])

            # write vars to disk
            elif c == 'w':
                write_vars(prog_vars)

            elif c == 'q':
                if dirty:
                    print('There are unsaved changes.')
                    print(':w to save; ^C to quit without saving.')
                else:
                    break

            elif c == '?':
                show_commands()

            else:
                print('unrecognized command: %s'%cmd)
        elif x == readchar.key.UP:
            adjust(cur_var, True)
            dirty = True
        elif x == readchar.key.DOWN:
            adjust(cur_var, False)
            dirty = True
        elif x == ' ':
            if dirty:
                exec(prog_source, globals())
                ns = main()
                print(ns)
                ns.trim(start, start+dur)
                ns.write_midi(prog_midi)
                numula.pianoteq_rpc.loadMidiFile(prog_midi)
                dirty = False
            numula.pianoteq_rpc.midiSeek(0)
            numula.pianoteq_rpc.midiPlay()

ipa_main()
