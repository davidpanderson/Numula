from note import *
import numpy, random

# --------------- Volume ----------------------

# we represent volume level as 0..1

ppp = .10
pp = .22
p = .34
mp = .46
mf = .58
f = .70
ff = .82
fff = .94

# linear volume change over a time interval
# is_closed: include notes at end of interval
#
def vol_seg(ns, vol0, vol1, dt, is_closed=True):
    start_time = ns.vol_cur_time
    end_time = start_time + dt
    dvol = vol1 - vol0
    if is_closed:
        end_time += epsilon
    else:
        end_time -= epsilon
    nnotes = len(ns.notes)
    while ns.vol_ind < nnotes:
        note = ns.notes[ns.vol_ind]
        if note.time > end_time:
            break;
        note.vol = vol0 + dvol*((note.time-start_time)/dt)
        ns.vol_ind += 1
    ns.vol_cur_time += dt

# ------- volume adjustments.  Changes are multiplicative factors

def vol_adjust(ns, atten, pred):
    for note in ns.notes:
        if pred(note):
            note.vol *= atten
            
def vol_adjust_func(ns, func, pred):
    for note in ns.notes:
        if pred(note):
            note.vol *= func(note)
            
# --------------- Timing ----------------------

# A tempo segment function.
# Such functions map score time to performance time over an interval starting at zero.
# args:
# dur: the length of the interval (in score time)
# time: a time in this interval (i.e. 0..dur)
# params: arguments to the function,
# e.g. in the case of linear tempo change, the start and end tempi
#
# This can be any monotonically increasing function.
# Linear is easy but something else (logarithmic, quadratic)
# might model performance practice better.
#
def linear(dur, time, params):
    tempo0 = params[0]
    tempo1 = params[1]
    dtempo = tempo1 - tempo0
    avg_tempo = tempo0 + .5*dtempo*time/dur
    seconds_per_beat = 60/avg_tempo
    #print('avg_tempo %f seconds_per_beat %f'%(avg_tempo, seconds_per_beat))
    return 4*seconds_per_beat*time

def tempo_seg(ns, dur, func, params):
    start_time = ns.cur_time
    end_time = ns.cur_time + dur
    while ns.cur_ind < len(ns.start_end):
        event = ns.start_end[ns.cur_ind]
        if event.time > end_time + epsilon:
            break
        dt = event.time - start_time
        t = ns.cur_perf_time + func(dur, dt, params)
        if event.kind == event_kind_note:
            note = event.obj
            if event.is_start:
                note.perf_time = t
            else:
                note.perf_dur = t - note.perf_time
        elif event.kind == event_kind_pedal:
            pedal = event.obj
            if event.is_start:
                pedal.perf_time = t
            else:
                pedal.perf_dur = t - pedal.perf_time
        else:
            raise Exception('bad event kind')
        ns.cur_ind += 1
    ns.cur_time += dur
    ns.cur_perf_time += func(dur, dur, params)

# ------- time adjustments.  Adjustments are to perf_time, and are in seconds

def pause_before(ns, t, dt):
    for note in ns.notes:
        if note.time + note.dur < t-epsilon:
            continue
        if note.time < t-epsilon:
            note.perf_dur += dt
        else:
            note.perf_time += dt
            note.perf_dur += dt

def pause_after(ns, t, dt):
    for note in ns.notes:
        if note.time < t-epsilon:
            if note.time + note.dur > t + epsilon:
                note.perf_dur += dt
            continue
        if note.time > t+epsilon:
            note.perf_time += dt
        else:
            note.perf_dur += dt
                
def roll_aux(chord, offsets, is_up, is_delay):
    if is_up:
        chord.sort(key=lambda x: x.pitch)
    else:
        chord.sort(key=lambda x: -x.pitch)
    # see which offsets are going to be used
    #
    mn = min(offsets[0:len(chord)])
    mx = max(offsets[0:len(chord)])
    dt = mx - mn
    ind = 0
    while ind < len(chord) and ind < len(offsets):
        note = chord[ind]
        off = offsets[ind] - mx
        note.perf_time += off
        note.perf_dur -= off
        if is_delay:
            note.perf_time += dt
        ind += 1
    return dt

def roll(ns, t, offsets, is_up=True, is_delay=False, pred=None, verbose=False):
    chord = []   # the notes at time t
    rolled = False
    for note in ns.notes:
        if note.time < t-epsilon: continue
        if note.time > t+epsilon:
            if not chord:
                break
            if not rolled:
                if verbose: print('roll ', offsets, list(map(lambda n: n.pitch, chord)))
                dt = roll_aux(chord, offsets, is_up, is_delay)
                rolled = True
            if not is_delay:
                break
            note.perf_time += dt
        else:
            if pred and not pred(note): continue
            chord.append(note)
    # chord might be at end of score
    #
    if chord and not rolled:
        roll_aux(chord, offsets, is_up, is_delay)

def t_adjust_list(ns, offsets, pred):
    ind = 0
    for note in ns.notes:
        if ind == len(offsets): break
        if pred(note):
            note.perf_time += offsets[ind]
            ind += 1

def t_adjust_notes(ns, offset, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_time += offset

def t_adjust_func(ns, func, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_time += func(note)

# perturb start time, and adjust duration to keep end time the same
# Possible TODO: adjust durations of earlier notes that end at this time
#
def t_random_uniform(ns, min, max, pred=None):
    for note in ns.notes:
        if pred and not pred(note): continue
        x = random.uniform(min, max)
        note.perf_time += x
        note.per_dur -= x

def t_random_normal(ns, stddev, max_sigma, pred=None):
    for note in ns.notes:
        if pred and not pred(note): continue
        while True:
            x = numpy.random.normal()
            if abs(x) < max_sigma: break
        y = stddev*x
        note.perf_time += y
        note.perf_dur -= y
                
# --------------- Articulation ----------------------

def score_dur_abs(ns, dur, pred):
    for note in ns.notes:
        if pred(note):
            note.dur = dur

def score_dur_rel(ns, factor, pred):
    for note in ns.notes:
        if pred(note):
            note.dur *= factor

def score_dur_func(ns, func, pred):
    for note in ns.notes:
        if pred(note):
            note.dur = func(note)
            
def perf_dur_abs(ns, dur, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_dur = dur

def perf_dur_rel(ns, factor, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_dur *= factor

def perf_dur_func(ns, func, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_dur = func(note)
