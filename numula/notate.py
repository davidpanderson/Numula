# utility functions for shorthand notations

import sys, os

def print_red(x: str):
    try:
        # in Idle
        color = sys.stdout.shell
        color.write(x, 'COMMENT')
    except AttributeError:
        # in terminal
        os.system('')
        CRED = '\033[91m'
        CEND = '\033[0m'
        print(CRED+x+CEND)
    print(' ', end='')

# in case of error, show context
def show_context(items: list[str], i: int):
    n = len(items)
    print('error in shorthand: ', end='')
    for j in range(i-5, i+6):
        if j<0: continue;
        if j>=n: continue;
        if j==i:
            print_red(items[j])
        else:
            print(items[j], end=' ')
    print('')

# expand '*4 foo *' into 'foo foo foo foo', with nesting
#
def expand_iter(items: list[str]) -> list[str]:
    if '*' not in items:
        return items

    # stacks
    nleft: list[int] = []
    start: list[int] = []

    out = []
    i = 0
    while i < len(items):
        t = items[i]
        if t == '*':
            if not nleft:
                show_context(items, i)
                raise Exception('unmatched *')
            nl = nleft[-1]
            if nl == 1:
                nleft.pop()
                start.pop()
            else:
                nleft[-1] = nl-1
                i = start[-1]
        elif t[0] == '*':
            try:
                nleft.append(int(t[1:]))
            except:
                show_context(items, i)
                raise Exception("can't parse %s"%t)
            start.append(i)
        elif '*' in t:
            show_context(items, i)
            raise Exception('bad token %s'%t)
        else:
            out.append(t)
        i += 1
    if nleft:
        j = start.pop()
        show_context(items, j)
        raise Exception('unclosed *n')
    return out

# expand macros in shorthand
# for now the only macro type is iteration (*n)
#
def expand_all(items: list[str]) -> list[str]:
    return expand_iter(items)

#############   stuff related to measures in shorthands   ##################

meas_dur = 0.
meas_prev_t = 0.     # time at last |n
meas_prev_m = 0     # measure no. at last |n
meas_first = True

# call this at start of processing shorthand string
#
def measure_init():
    global meas_first, meas_dur
    meas_first = True
    meas_dur = 0.

# process a shorthand item starting with |
# if item is of the form |M (measure number)
# verify that t (current time) corresponds to that measure
#
def comment(item, t: float):
    global meas_dur, meas_prev_t, meas_prev_m, meas_first

    if not item[1:].isnumeric(): return
    if meas_dur == 0.: return
    m = int(item[1:])
    if meas_first:
        meas_prev_t = t
        meas_prev_m = m
        meas_first = False
        return

    # compare time since last |n with expected time
    #
    dt = t - meas_prev_t
    dm = m - meas_prev_m
    if abs(dm*meas_dur - dt) > 1e-5:
        raise Exception('Inconsistent measure number: %f != %f'%(
            m, meas_prev_m + dt/meas_dur))
    meas_prev_t = t
    meas_prev_m = m

# process an item s of the form meas4/4
#
def set_measure_dur(s: str, t: float):
    global meas_first, meas_prev_t, meas_dur
    if not meas_first and t > meas_prev_t:
        raise Exception("|n required before setting new measure length")
    x = s[4:]
    a = x.split('/')
    try:
        num = int(a[0])
        denom = int(a[1])
    except:
        print('bad measure dur: ', s)
        return False
    meas_dur = num/denom
    return True

# set the measure duration globally
# (so you don't need meas4/4 in shorthands)
#
def measure_duration(t: float):
    global meas_dur
    meas_dur = t
