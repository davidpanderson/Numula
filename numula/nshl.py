# declare an adjustable variable
# val: initial value
# inc: increment
# lo, hi: min/max values
#
# Note: adding the var to globals() makes it visible only in this module.
# I can't figure out how to make it visible outside.
# So for now the main program has to import nshl
# and refer to the variable as nshl.x

vars = {}   # the list of adjustable variables

def var(name, val, inc, lo=0, hi=1):
    if name not in globals():
        globals()[name] = val
    vars[name] = {'inc': inc, 'lo': lo, 'hi': hi}

def get(name):
    return globals()[name]

def set(name, val):
    globals()[name] = val
