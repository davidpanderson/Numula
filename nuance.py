from note import *
import numpy


# --------------- Volume ----------------------

# we represent volume level as 0..1

ppp = .01
pp = .14
p = .28
mp = .42
mf = .56
f = .70
ff = .84
fff = .99

def vol_init(ns):
    ns.cur_time = 0
    ns.ind = 0

# linear volume change over a time interval
# is_closed: include notes at end of interval
#
def vol_seg(ns, vol0, vol1, dt, is_closed=True):
    start_time = ns.cur_time
    end_time = start_time + dt
    dvol = vol1 - vol0
    if is_closed:
        end_time += epsilon
    else:
        end_time -= epsilon
    nnotes = len(ns.notes)
    while ns.ind < nnotes:
        note = ns.notes[ns.ind]
        if note.time > end_time:
            break;
        note.vol = vol0 + dvol*((note.time-start_time)/dt)
        ns.ind += 1
    ns.cur_time += dt

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

# make an auxiliary structure with start/end events
#
def timing_init(ns):
    ns.start_end = []
    for note in ns.notes:
        start = [note.time, note, True]
        end = [note.time+note.dur, note, False]
        ns.start_end.append(start)
        ns.start_end.append(end)
    ns.start_end.sort(key=lambda x: x[0])
    ns.cur_ind = 0    # index into ns.start_end
    ns.cur_time = 0
    ns.cur_perf_time = 0
    
def linear(dur, time, params):
    tempo0 = params[0]
    tempo1 = params[1]
    dtempo = tempo1 - tempo0
    avg_tempo = tempo0 + .5*dtempo*time/dur
    seconds_per_beat = 60/avg_tempo
    #print('avg_tempo %f seconds_per_beat %f'%(avg_tempo, seconds_per_beat))
    return 4* seconds_per_beat * time

def tempo_seg(ns, dur, func, params):
    start_time = ns.cur_time
    end_time = ns.cur_time + dur
    while ns.cur_ind < len(ns.start_end):
        event = ns.start_end[ns.cur_ind]
        if event[0] > end_time + epsilon:
            break
        dt = event[0] - start_time
        t = ns.cur_perf_time + func(dur, dt, params)
        note = event[1]
        if event[2]:
            note.perf_time = t
        else:
            note.perf_dur = t - note.perf_time
        ns.cur_ind += 1
    ns.cur_time += dur
    ns.cur_perf_time += func(dur, dur, params)

# ------- adjustments start here.  adjustments are to perf_time, and are in seconds

def pause(ns, t, dt, before):
    if before:
        for note in ns.notes:
            if note.time + note.dur < t-epsilon:
                print('skip')
                continue
            if note.time < t-epsilon:
                note.perf_dur += dt
            else:
                note.perf_time += dt
                note.perf_dur += dt
    else:
        for note in ns.notes:
            if note.time < t-epsilon:
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

def roll(ns, t, offsets, is_up, is_delay):
    chord = []   # the notes at time t
    rolled = False
    for note in ns.notes:
        if note.time < t-epsilon: continue
        if note.time > t+epsilon:
            if not chord:
                break
            if not rolled:
                dt = roll_aux(chord, offsets, is_up, is_delay)
                rolled = True
            if not is_delay:
                break
            note.perf_time += dt
        else:
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

def t_adjust_notes_func(ns, func, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_time += func(note)

def t_random_uniform(ns, min, max, pred):
    for note in ns.notes:
        if pred(note):
            note.perf_time += random.uniform(min, max)

def t_random_normal(ns, stddev, max_sigma, pred):
    for note in ns.notes:
        while True:
            x = numpy.random.normal()
            if abs(x) < max_sigma: break
        note.perf_time += stddev*x
                
# --------------- Articulation ----------------------

def dur_abs(ns, dur, pred):
    for note in ns.notes:
        if pred(note):
            note.dur = dur

def dur_rel(ns, factor, pred):
    for note in ns.notes:
        if pred(note):
            note.dur *= factor

# --------------- Utility --------------------

# tag notes that are the highest or lowest sounding notes at their start
#
def flag_outer_aux(active, started):
    print('flag_aux: %d active, %d started'%(len(active), len(started)))
    min = 128
    max = -1
    for n in active:
        if n.pitch < min: min = n.pitch
        if n.pitch > max: max = n.pitch
    for n in started:
        if n.pitch == max:
            n.tags.append('highest')
        if n.pitch == min:
            n.tags.append('lowest')
        
def flag_outer(ns):
    cur_time = 0
    active = []     # notes active at current time
    started = []    # notes that started at current time
    for note in ns.notes:
        if note.time > cur_time + epsilon:
            if len(started):
                flag_outer_aux(active, started)
            cur_time = note.time
            new_active = [note]
            for n in active:
                if n.time + n.dur > cur_time + epsilon:
                    new_active.append(n)
            active = new_active
            started = [note]
        else:
            active.append(note)
            started.append(note)
    flag_outer_aux(active, started)

