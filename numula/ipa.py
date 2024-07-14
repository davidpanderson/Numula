# val: initial value
# step: adjustment increment
# lo, hi: min/max values
#
# Note: adding the var to globals() makes it visible only in this module.
# I can't figure out how to make it visible outside.
# So for now the main program has to import ipa
# and refer to the variable as ipa.x

vars = []   # list of adjustable variables

# declare an adjustable variable
def var(
    name,               # variable name
    val,                # initial value
    step,               # adjustment increment (if numeric)
    lo, hi,             # min/max values (if numeric)
    adjustable=True,    # if False, don't show or allow change
    numeric = True,     # if False, can assign but not inc/dev
    desc=None           # textual description
):
    if name in globals():
        return
    globals()[name] = val
    if adjustable:
        vars.append(
            {'name': name,
                'step': step,
                'lo': lo,
                'hi': hi,
                'numeric': numeric,
                'desc': desc
            }
        )

# volume variable
#
def vvar(name, val, adjustable=True, desc=None):
    var(name, val, .1, 0, 2, adjustable, True, desc)

# tempo variable
#
def tvar(name, val, adjustable=True, desc=None):
    var(name, val, 3, 10, 200, adjustable, True, desc)

# delay variable
#
def dvar(name, val, adjustable=True, desc=None):
    var(name, val, .02, 0, 1, adjustable, True, desc)

# time interval variable (text, like 2/1)
#
def ivar(name, val, adjustable=True, desc=None):
    var(name, val, 0,0,0, adjustable=adjustable, numeric=False, desc=desc)

def get(name):
    return globals()[name]

def set(name, val):
    globals()[name] = val

# read variable values from file
#
def read_vars(fname):
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            [name, val] = line.split()
            try:
                set(name, float(val))
            except:
                set(name, val)
