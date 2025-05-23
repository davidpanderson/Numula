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
# :i                set current var to the ith one
# :i val            assign value to ith var
# :s                show vars and start/dur
# :w                write var values to prog.vars
# :?                show commands
# space             play from start to start+dur
# up/down arrow     inc/dec current var

import sys, time, os
import readchar
import numula_path
import numula.pianoteq
import numula.ipa as ipa

def show_commands():
    print('''
commands:
:i                set current var to the ith one
:i val            assign value to ith var
:s                show vars and start/dur
:w                write var values to prog.vars
:?                show commands
space             play from start to start+dur
up/down arrow     inc/dec current var
    ''')

def type_name(type: int):
    if type == ipa.IPA_VOL: return 'Volume'
    if type == ipa.IPA_VOL_MULT: return 'Volume multiplier'
    if type == ipa.IPA_DT_SCORE: return 'Score time'
    if type == ipa.IPA_DT_SEC: return 'Seconds'
    if type == ipa.IPA_TEMPO: return 'Tempo'
    if type == ipa.IPA_BOOL: return 'Boolean'
    if type == ipa.IPA_LAYER: return 'Layer'
    return '???'

# rows: list of lists of n strings
# print them so that columns line up
#
def print_table(rows: list[list[str]], n: int):
    width = [0]*n
    for row in rows:
        for i in range(n):
            x = len(row[i])
            if x > width[i]: width[i] = x
    codes = []
    for i in range(n):
        codes.append('{0:%ds}'%width[i])
    for row in rows:
        y: list[str] = []
        for i in range(n):
            y.append(codes[i].format(row[i]))
        print('  '.join(y))

# show non-hidden variables
#
def show_vars(cur_var: int):
    print('variables:')
    n = len(ipa.vars)
    rows = [['#', 'name', 'value', 'type', 'tags', 'description']]
    for i in range(n):
        row = ['']*6
        row[0] = str(i+1)
        if i == cur_var:
            row[0]+='*'
        x = ipa.vars[i]
        name = x['name']
        row[1] = name
        if ipa.numeric(x['type']):
            row[2] = '{0:.2f}'.format(ipa.get(name))
        else:
            row[2] = str(ipa.get(name))
        row[3] = type_name(x['type'])
        if x['tags']:
            if ipa.should_hide_var(x):
                continue
            row[4] = ', '.join(x['tags'])
        row[5] = x['desc']
        rows.append(row)
    print_table(rows, 6)

# write adjustable variables to a file
#
def write_vars(fname: str):
    with open(fname, 'w') as f:
        for var in ipa.vars:
            name = var['name']
            if ipa.numeric(var['type']):
                f.write('%s %f\n'%(name, ipa.get(name)))
            else:
                f.write('%s %s\n'%(name, ipa.get(name)))

# inc or dec a numeric adjustable variable
#
def adjust(ivar: int, up: bool):
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
    print('%s: %.2f'%(name ,val))

def ipa_main():
    global ns
    global __name__
    __name__ = 'foo'
    if len(sys.argv) != 2:
        raise Exception('usage: dipa prog')
    prog_path = sys.argv[1]
    prog = os.path.basename(prog_path)
    prog_vars = ipa.vars_file_path(prog)
    prog_midi = 'data/%s.midi'%(prog)

    # run the program to get its adjustable variables
    #
    with open(prog_path+'.py') as f:
        prog_source = f.read()
    exec(prog_source, globals())
    ns = main()
    try:
        ipa.vars
    except:
        raise Exception('no adjustable vars')
    cur_var = -1
    n = len(ipa.vars)
    for i in range(n):
        x = ipa.vars[i]
        if numeric(x['type']):
            cur_var = i
            break

    if os.path.exists(prog_vars):
        print('reading values from ', prog_vars)
        ipa.read_vars(prog)

    ipa.var('start', IPA_DT_SCORE, '0/1', desc='playback start time')
    ipa.var('dur', IPA_DT_SCORE, '1/1', desc='playback duration')
    ipa.var('show', IPA_BOOL, False, desc='show score on playback')
    show_vars(cur_var)

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
                    if len(words) > 1:
                        w = words[1]
                        try:
                            x = float(w)
                        except:
                            print('bad value ', w)
                            continue
                        if ipa.valid_value(x, v['type']):
                            ipa.set(v['name'], x)
                        else:
                            print('bad value ', w)
                            continue
                        dirty = True
                    else:
                        print('%s: %f'%(v['name'], ipa.get(v['name'])))
                    cur_var = j
                else:
                    if len(words) < 2:
                        print('must supply a value')
                        continue
                    w = words[1]
                    if v['type'] == IPA_BOOL:
                        if w == 't':
                            ipa.set(v['name'], True)
                        elif w == 'f':
                            ipa.set(v['name'], False)
                        else:
                            print('bad value: use t/f')
                            continue
                    else:
                        if ipa.valid_value(w, v['type']):
                            ipa.set(v['name'], w)
                        else:
                            print('bad value ', w)
                            continue
                    dirty = True

            # show commands
            elif words[0] == 's':
                show_vars(cur_var)

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
            if dirty or ipa.get('show'):
                print('computing score')
                exec(prog_source, globals())
                ns = main()
                s = ipa.fraction_value(ipa.get('start'))
                d = ipa.fraction_value(ipa.get('dur'))
                ns.trim(s, s+d)
                if ipa.get('show'):
                    print(ns)
                ns.write_midi(prog_midi)
                numula.pianoteq.loadMidiFile(prog_midi)
                dirty = False
            numula.pianoteq.midiSeek(0)
            numula.pianoteq.midiPlay()

ipa_main()
