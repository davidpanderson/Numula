# nsh: iteractively edit nuance params in a Numula program
#
# You can select the param you want to vary,
# then use the up and down arrows to change its value.
# When you hit the space bar, it plays a selected part the piece.
#
# usage: nsh prog
#
# The program (prog.py) must:
# 1) declare adjustable variables with
#   nvar(name, val, inc, lo=0, hi=1)
#   It can refer to these as 'nshl.name'
#   (ideally it should just be 'name', but I can't figure out how).
# 2) Create a global var 'ns' containing a ScoreBasic
#
# commands:
# :t start dur      set playback start/dur (default 0, 1)
# :v name           set current var to name
# :s                show vars and start/dur
# :w                write var values to prog.nvars
# space             play from start to end
# up/down arrow     inc/dec current var

import sys, time, os
import readchar
import numula.pianoteq
import numula.pianoteq_rpc
import nshl

def show(cur_var, start, dur):
    print('adjustable variables:')
    for key in nshl.vars:
        x = nshl.vars[key]
        print('name: %s value %f inc %f min %f max %f'%(key, nshl.get(key), x['inc'], x['lo'], x['hi']))
    print('current var: '+cur_var)
    print('start: %f dur: %f'%(start, dur))
 
# inc or dec an adjustable variable
#
def adjust(var, up):
    x = nshl.vars[var]
    val = nshl.get(var)
    if up:
        val += x['inc']
        if val > x['hi']:
            val = x['hi']
    else:
        val -= x['inc']
        if val < x['lo']:
            val = x['lo']
    nshl.set(var, val)
    print('%s: %f'%(var ,val))

def nsh_main():
    if len(sys.argv) != 2:
        raise Exception('usage: nsh prog')
    prog = sys.argv[1]
    prog_py = prog+'.py'
    prog_vars = prog+'.vars'
    prog_midi = 'data/%s.mid'%(prog)

    # run the program to get its adjustable variables
    #
    with open(prog_py) as f:
        prog_source = f.read()
    exec(prog_source, globals())
    try:
        nshl.vars
    except:
        raise Exception('no adjustable vars')
    for var in nshl.vars:
        cur_var = var
        break

    try:
        ns
    except:
        raise Exception('no score')

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
            if c == 'v':
                var = cmd[2:]
                if var not in nshl.vars:
                    print('no adjustable variable '+var)
                    continue
                cur_var = var
            elif c == 's':
                show(cur_var, start, dur)
            elif c == 't':
                x = cmd.split()
                if len(x) != 3:
                    print('usage: :t start dur')
                    continue
                start = float(x[1])
                dur = float(x[2])
            elif c == 'w':
                write_vars(prog_vars)
            else:
                print('unrecognized command: %s'%cmd)
        elif x == readchar.key.UP:
            print('up arrow')
            adjust(cur_var, True)
            dirty = True
        elif x == readchar.key.DOWN:
            print('down arrow')
            adjust(cur_var, False)
            dirty = True
        elif x == ' ':
            if dirty:
                exec(prog_source)
                ns.trim(start, start+dur)
                ns.write_midi(prog_midi)
                numula.pianoteq_rpc.loadMidiFile(prog_midi)
                dirty = False
            numula.pianoteq_rpc.midiSeek(0)
            numula.pianoteq_rpc.midiPlay()

nsh_main()
