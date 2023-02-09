# utility functions for shorthand notation

import sys, os

def print_red(x):
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
def show_context(items, i):
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
def expand_iter(items):
    if '*' not in items:
        return items

    # stacks
    nleft = []
    start = []

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
                raise Exception("can't parse "%t)
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

# if item is of the form |M (measure number)
# verify that dt corresponds to that measure
meas_dur = 0
meas_prev_t = 0
meas_prev_m = 0
meas_first = True

def measure_init():
    global meas_first, meas_dur
    meas_first = True
    meas_dur = 0

def comment(item, t):
    global meas_dur, meas_prev_t, meas_prev_m, meas_first

    if not item[1:].isnumeric(): return
    if meas_dur == 0: return
    m = float(item[1:])
    if meas_first:
        meas_prev_t = t
        meas_prev_m = m
        meas_first = False
        return
    dt = t - meas_prev_t
    dm = m - meas_prev_m
    if abs(dm*meas_dur - dt) > 1e-5:
        raise Exception('Inconsistent measure number: %f != %f'%(
            m, meas_prev_m + dt/meas_dur))
    meas_prev_t = t
    meas_prev_m = m

# s is of the form m4/4
#
def set_measure_dur(s, t):
    global meas_first, meas_prev_t, meas_dur
    if not meas_first and t > meas_prev_t:
        raise Exception("Can't set measure length in the middle of a measure")
    t = s[1:]
    a = t.split('/')
    print(s, t)
    print(a[0], a[1])
    try:
        num = int(a[0])
        denom = int(a[1])
    except:
        print(t)
        return False
    meas_dur = num/denom
    return True
    
def expand_all(items):
    return expand_iter(items)
