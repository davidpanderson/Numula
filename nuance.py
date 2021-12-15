from note import *

def score_start(ns):
    ns.cur_time = 0
    ns.ind = 0

# --------------- Dynamics ----------------------

# we represent dynamic level as 0..1

ppp = .01
pp = .14
p = .28
mp = .42
mf = .56
f = .70
ff = .84
fff = .99

def vol(ns, vol0, vol1, dt, is_closed=True):
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

# mark notes that are the highest or lowest sounding notes at their start
#
def flag_aux(active, started):
    min = 128
    max = -1
    for n in active:
        if n.pitch < min: min = n.pitch
        if n.pitch > max: max = n.pitch
    for n in started:
        n.highest = n.pitch == max
        n.lowest = n.pitch == min
        
def flag_outer(ns):
    cur_time = 0
    active = []     # notes active at current time
    started = []    # notes that started at current time
    for note in ns.notes:
        if note.time > cur_time + epsilon:
            if len(started):
                flag_aux(active, started)
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
    flag_aux(active, started)
        
def outer(ns, bottom, mid, top, dt):
    end_time = ns.cur_time + dt
    while ns.ind < len(ns.notes):
        note = ns.notes[ns.ind]
        if note.time > end_time:
            break
        if note.highest:
            note.vol *= top
        elif note.lowest:
            note.vol *= bottom
        else:
            note.vol *= mid
    ns.cur_time += dt

# --------------- Timing ----------------------

# make an auxiliary structure with start/end events
#
def make_start_end(ns):
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
    tempo0 = 1/params[0]
    tempo1 = 1/params[1]
    dtempo = tempo1 - tempo0
    avg_tempo = tempo0 + .5*t/dur
    return avg_tempo * time

def tseg(ns, dur, func, params):
    start_time = ns.cur_time
    end_time = ns.cur_time + dur
    while ns.cur_ind < len(ns.start_end):
        event = ns.start_end[ns.cur_ind]
        if event[0] > end_time + epsilon:
            break
        dt = event[0] - start_time
        t = cur_perf_time + func(dur, dt, params)
        note = event[1]
        if event[2]:
            note.perf_time = t
        else:
            note.perf_dur = t - note.perf_time
        ns.cur_ind += 1
    ns.cur_time += dur
    ns.cur_perf_time += func(dur, dur, params)

# --------------- Articulation ----------------------
