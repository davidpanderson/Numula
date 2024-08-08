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
        if v['type'] != IPA_BOOL:
            raise Exception('tag %s not bool'%tag)

# are all the tags in the list True?
#
def tags_set(tag_list):
    for x in tag_list:
        if not globals()[x]:
            return False
    return True

def numeric(type):
    return type in [IPA_VOL, IPA_VOL_MULT, IPA_TEMPO, IPA_DT_SEC]

# declare an adjustable variable
# val: initial value
# step: adjustment increment
# lo, hi: min/max values
#
# Note: adding the var to globals() makes it visible only in this module.
# Someday I'll figure out how to make it visible outside.
# Until then, the main program has to do
#
# from ipa import *
#
# after declaring variables

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
    # TODO: check validity of 'val'
    if type == IPA_VOL:
        if val is None: val = .5
        var_aux(name, val, .02, 0, 1, tags, type, desc);
    elif type == IPA_VOL_MULT:
        if val is None: val = 1
        var_aux(name, val, .04, 0, 2, tags, type, desc);
    elif type == IPA_DT_SCORE:
        if val is None: val = '1/1'
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    elif type == IPA_DT_SEC:
        if val is None: val = 0
        var_aux(name, val, .01, -1, 1, tags, type, desc);
    elif type == IPA_TEMPO:
        if val is None: val = 60
        var_aux(name, val, 2, 10, 200, tags, type, desc);
    elif type == IPA_BOOL:
        if val is None: val = True
        var_aux(name, val, 0, 0, 0, tags, type, desc);
    else:
        raise Exception('bad IPA type %s'%type)

def get(name):
    return globals()[name]

def set(name, val):
    globals()[name] = val

def vars_file_path(prog_name):
    return 'data/%s.vars'%prog_name

# read variable values from file
#
def read_vars(prog_name):
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
