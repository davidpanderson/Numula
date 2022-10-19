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
mstart = 0
def comment(item, dt, mdur):
    global mstart
    if not item[1:].isnumeric(): return
    if mdur == 0: return
    m1 = float(item[1:])
    if dt == 0:
        mstart = m1
        return
    m2 = mstart + dt/mdur
    if abs(m1-m2) > 1e-5:
        raise Exception('Inconsistent measure number: %f != %f'%(m1, m2))
    
def expand_all(items):
    return expand_iter(items)
