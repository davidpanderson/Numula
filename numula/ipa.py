vars = []   # list of adjustable variables
            # their values are stored in globals()

VOL = 1
DUR = 2
TEMPO = 3
PAUSE = 4
BOOL = 5

def var_lookup(name):
    for v in vars:
        if v['name'] == name:
            return v
    return None

def check_tags_defined(tag_list):
    for tag in tag_list:
        v = var_lookup(tag)
        if not v:
            raise Exception('tag %s not defined'%tag)
        if v['type'] != BOOL:
            raise Exception('tag %s not bool'%tag)

# are all the tags in the list True?
#
def tags_set(tag_list):
    for x in tag_list:
        if not globals()[x]:
            return False
    return True

def numeric(type):
    return type in [VOL, TEMPO, PAUSE]

# declare an adjustable variable
# val: initial value
# step: adjustment increment
# lo, hi: min/max values
#
# Note: adding the var to globals() makes it visible only in this module.
# I can't figure out how to make it visible outside.
# So for now the main program has to import ipa
# and refer to the variable as ipa.x

def var_aux(
    name,               # variable name
    val,                # initial value
    step,               # adjustment increment (if numeric)
    lo, hi,             # min/max values (if numeric)
    tags,
    type,
    desc                # textual description
):
    if name in globals():
        return
    check_tags_defined(tags)
    globals()[name] = val
    vars.append(
        {
            'name': name,
            'step': step,
            'lo': lo,
            'hi': hi,
            'tags': tags,
            'type': type,
            'desc': desc
        }
    )

def var (
    name,
    type,
    val = None,
    tags = [],
    desc = None
):
    if type == VOL:
        if val is None: val = 1
        var_aux(name, val, .03, 0, 2, tags, type, desc);
    elif type == TEMPO:
        if val is None: val = 60
        var_aux(name, val, 3, 10, 200, tags, type, desc);
    elif type == PAUSE:
        if val is None: val = 0
        var_aux(name, val, .02, 0, 1, tags, type, desc);
    elif type == DUR:
        if val is None: val = '1/1'
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    elif type == BOOL:
        if val is None: val = True
        var_aux(name, val, 0, 0, 0, tags, type, desc);

def get(name):
    return globals()[name]

def set(name, val):
    globals()[name] = val

# read variable values from file
#
def read_vars(name):
    fname = name+'.vars'
    import os
    if not os.path.exists(fname):
        return
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            [name, val] = line.split()
            try:
                set(name, float(val))
            except:
                set(name, val)
