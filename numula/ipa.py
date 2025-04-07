# Interactive Parameter Adjustment (IPA)
# a system for efficiently adjusting nuance parameters
# see: https://github.com/davidpanderson/numula/wiki/Interactive-parameter-adjustment

import os

vars = []   # list of adjustable variables
            # their values are stored in globals()

# variable types.  Each has default min/mix and step size

IPA_VOL = 1
    # volume, absolute or increment: 0..1
IPA_VOL_MULT = 2
    # volume multiplier: 0..2
IPA_DT_SCORE = 3
    # score-time interval, as a string like '1/4'
IPA_DT_SEC = 4
    # time interval in seconds, e.g. of a pause
IPA_TEMPO = 5
    # beats per minute, or relative to 60
IPA_BOOL = 6
    # typically used for section tags
IPA_LAYER = 7
    # tag for a nuance layer: on/hide/off

def var_lookup(name: str):
    for v in vars:
        if v['name'] == name:
            return v
    return None

def check_tags_defined(tag_list: list[str]):
    for tag in tag_list:
        v = var_lookup(tag)
        if not v:
            raise Exception('tag %s not defined'%tag)
        if v['type'] not in (IPA_BOOL, IPA_LAYER):
            raise Exception('tag %s not IPA_BOOL or IPA_LAYER'%tag)

# is the var hidden given tag values?
#
def should_hide_var(var: str):
    for x in var['tags']:
        v2 = var_lookup(x)
        if v2['type'] == IPA_BOOL:
            if not globals()[x]:
                return True
        if v2['type'] == IPA_LAYER:
            if globals()[x] != 'on':
                return True
    return False

def numeric(type: int):
    return type in (IPA_VOL, IPA_VOL_MULT, IPA_TEMPO, IPA_DT_SEC)

def fraction_value(str: str):
    a = str.split('/')
    try:
        num = int(a[0])
        denom = int(a[1])
    except:
        return None
    if denom <= 0: return None
    if num < 0: return None
    return num/denom

def valid_value(val, t):
    if t == IPA_BOOL:
        return isinstance(val, bool)
    if numeric(t):
        if type(val) not in [int, float]: return False
    if t == IPA_VOL:
        return 0 <= val <= 1
    if t == IPA_VOL_MULT:
        return 0 <= val <= 2
    if t == IPA_TEMPO:
        return 1 < val < 1000
    if t == IPA_DT_SEC:
        return 0 <= val <= 10
    if t == IPA_DT_SCORE:
        if not isinstance(val, str): return False
        return fraction_value(val) is not None
    if t == IPA_LAYER:
        return val in ('on', 'hide', 'off')

# declare an adjustable variable
# val: initial value
# step: adjustment increment
# lo, hi: min/max values
#
# Note: adding the var to globals() makes it visible only in this module.
# Someday I'll figure out how to make it visible outside.
# Until then, the main program has to do
#   from ipa import *
# after declaring variables

def var_aux(
    name: str,              # variable name
    val: Any,               # initial value
    step: float,            # adjustment increment (if numeric)
    lo: float, hi: float,   # min/max values (if numeric)
    tags: list[str],
    type: int,
    desc: str               # textual description
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
    name: str,
    type: int,
    val: Any,
    tags: list[str] = [],
    desc: str = ''
):
    if type == IPA_VOL:
        var_aux(name, val, .02, 0, 1, tags, type, desc);
    elif type == IPA_VOL_MULT:
        var_aux(name, val, .04, 0, 2, tags, type, desc);
    elif type == IPA_DT_SCORE:
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    elif type == IPA_DT_SEC:
        var_aux(name, val, .01, -1, 1, tags, type, desc);
    elif type == IPA_TEMPO:
        var_aux(name, val, 2, 1, 1000, tags, type, desc);
    elif type == IPA_BOOL:
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    elif type == IPA_LAYER:
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    else:
        raise Exception('bad IPA type %s'%type)

def get(name: str):
    return globals()[name]

def set(name: str, val: Any):
    globals()[name] = val

def vars_file_path(prog_name: str) -> str:
    return 'data/%s.vars'%prog_name

# read variable values from file
#
def read_vars(prog_name: str):
    path = vars_file_path(prog_name)
    if not os.path.exists(path):
        return
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            [name, val] = line.split()
            try:
                set(name, float(val))
            except:
                set(name, val)
