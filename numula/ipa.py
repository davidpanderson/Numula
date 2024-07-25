vars = []   # list of adjustable variables
            # their values are stored in globals()
tags = []   # list of {name, value} dicts
tag_names = []

def tag(name, value=True):
    if name in tag_names:
        raise Exception('tag already defined: %s'%name)
    tags.append(
        {
            'name': name,
            'value': value
        }
    )
    tag_names.append(name)

def check_tags_defined(tag_list):
    for tag in tag_list:
        if not tag in tag_names:
            raise Exception('tag %s not defined'%tag)

# are all the tags in the list True?
#
def tags_set(tag_list):
    for x in tags:
        if not x['value']:
            if x['name'] in tag_list:
                return False
    return True

def get_tag(tag):
    for x in tags:
        if x['name'] == tag:
            return x['value']
    raise Exception('no tag %s'%tag)
        

def set_tag(tag, val):
    for x in tags:
        if x['name'] == tag:
            x['value'] = value
            return
    raise Exception('no tag %s'%tag)

VOL = 1
DUR = 2
TEMPO = 3
PAUSE = 4
BOOL = 5

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
        var_aux(name, val, .1, 0, 2, tags, type, desc);
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
def read_vars(fname):
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            [name, val] = line.split()
            try:
                set(name, float(val))
            except:
                set(name, val)
