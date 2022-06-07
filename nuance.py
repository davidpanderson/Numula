# This file is part of Numula
# Copyright (C) 2022 David P. Anderson
#
# Numula is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Numula is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Numula.  If not, see <http://www.gnu.org/licenses/>.

import numpy, random, copy
from note import *

class linear:
    def __init__(self, y0, y1, dt, closed_start=True, closed_end=False):
        self.y0 = y0
        self.y1 = y1
        self.dy = y1 - y0
        self.dt = dt
        self.closed_start = closed_start
        self.closed_end = closed_end
    def val(self, t):
        return self.y0 + self.dy*(t/self.dt)
    def integral(self, t):
        return t*(self.y0+self.val(t))/2
    def integral_total(self):
        return self.dt*(self.y0+self.y1)/2
    # convert from tempo function in BPM
    # to 1-centered inverse tempo function
    def bpm(self):
        self.y0 = 60/self.y0
        self.y1 = 60/self.y1
        self.dy = self.y1 - self.y0

# Dirac delta; used in tempo PFTs to represent pauses
# if after is True, pause goes after notes at that time
class delta:
    def __init__(self, value, after=True):
        self.value = value
        self.after = after
        self.dt = 0
    def bpm(self):
        self.value /= 4
    def integral_total(self):
        return self.value

#from pprint import pprint

# make sure the pft has well-defined values at segment boundaries
def pft_check_closure(pft):
    n = len(pft)
    for i in range(n-1):
        seg0 = pft[i]
        seg1 = pft[i+1]
        if seg0.closed_end:
            if seg1.closed_start and seg0.y1 != seg1.y0:
                raise Exception('conflicting values in PFT')
        else:
            if not seg1.closed_start:
                raise Exception('missing value in PFT')

# score-time duration of a PFT
def pft_dur(pft):
    dt = 0
    for seg in pft:
        dt += seg.dt
    return dt

# average value of pft
def pft_avg(pft):
    sum = 0
    for seg in pft:
        sum += seg.integral_total()
    return sum/pft_dur(pft)

# convert tempo PFT from BPM units
def pft_bpm(pft):
    for seg in pft:
        seg.bpm()

# class for getting the values of a PFT at increasing times
class pft_value:
    def __init__(self, pft):
        self.pft = pft
        self.ind = 0            # index of current seg
        self.prev_dur = 0       # duration of previous segs

    def value(self, t):
        dt = t - self.prev_dur
        while True:
            seg = self.pft[self.ind]
            if dt < seg.dt - epsilon:
                return seg.val(dt)
            if dt < seg.dt + epsilon and seg.closed_end:
                return seg.y1
            dt -= seg.dt
            self.prev_dur += seg.dt
            self.ind += 1
            if self.ind == len(self.pft):
                raise Exception('past end of PFT: t %f'%t)
            
# ------------------- Dynamics ------------------------

ppp = .15
pp = .4
p = .65
mp = .9
mf = 1.05
f = 1.3
ff = 1.55
fff = 1.8

# adjust volume of selected notes by PFT starting at t0
def vol_adjust_pft(self, pft, t0=0, pred=None):
    pft_check_closure(pft)
    seg_ind = 0
    seg = pft[0]
        # which segment we're on
    seg_start = t0
        # start time of that segment
    seg_end = t0 + seg.dt
    t_end = t0 + pft_dur(pft)
        # end time of function
    for n in self.notes:
        if n.time > t_end + epsilon:
            break
        if n.time < t0 - epsilon:
            continue
        if pred and not pred(n):
            continue
        while True:
            # skip segments as needed
            if n.time < seg_end - epsilon:
                v = seg.val(n.time - seg_start)
                break
            if n.time < seg_end + epsilon:
                # note is at end of this seg
                if seg.closed_end:
                    v = seg.y1
                    break
                if seg_ind == len(pft)-1:
                    return
            # move to next seg
            seg_start += seg.dt
            seg_ind += 1
            seg = pft[seg_ind]
            seg_end = seg_start + seg.dt
        # v is the adjustment factor
        n.vol *= v
        
def vol_adjust(self, atten, pred):
    for note in self.notes:
        if pred(note):
            note.vol *= atten
            
def vol_adjust_func(self, func, pred):
    for note in self.notes:
        if pred(note):
            note.vol *= func(note)
            
# ------------------- Timing ------------------------

# adjust the timing of selected notes and pedal events.
# pft is a tempo function, which can contain segments (such as linear)
# and Dirac deltas.
# If bpm is False, its value is performance time per unit score time;
# larger is slower.
# If bpm is True, its value is inverted, so that larger is faster
# (60 = no change, 120 = speed up by 2X)
# In both cases, the value of Dirac deltas is in performance time.
#
# Apply the PFT, starting at score time t0, to the selected notes.
#
# If "normalize" is True, scale the PFT so that its average is 1.
#
# Implementation:
# - make a time-sorted list of start/end "events"
#   for the notes and pedals,
#   each with (score) time and a perf time.
# - for each successive pair of events A and B,
#   compute average of the PFT between the score times of A and B.
#   scale the perf time interval between A and B by this.
# - update the (perf) time and dur of the corresponding Note and Pedal objects.
#
def tempo_adjust_pft(self, _pft, t0=0, pred=None, normalize=False, bpm=True):
    debug = False

    if bpm:
        pft = copy.deepcopy(_pft)
        pft_bpm(pft)    # invert tempo function
    else:
        pft = copy.copy(_pft)

    self.make_start_end_events()

    # keep track of our position in the PFT, and the integral so far
    seg_ind = 0
    seg = pft[0]
    seg_start = t0
    seg_end = t0 + seg.dt
    pft_end = t0 + pft_dur(pft)
    seg_integral = 0        # integral up to current seg

    scale_factor = 1
    if normalize:
        scale_factor = 1/pft_avg(pft)
        if debug: print('scale factor: ', scale_factor)
        
    # append infinite unity segment
    # needed to handle note-end events that lie beyond PFT domain
    pft.append(linear(1, 1, 9999999))
    
    # loop over events.
    # keep track of params of previous event
    #
    prev_time = 0       # its score time
    prev_perf = 0       # its perf time
    prev_perf_adj = 0   # its adjusted perf time
    prev_integral = 0   # integral of pft at that point
    for event in self.start_end:
        if debug: print('event time %f perf time %f prev_time %f'%(event.time, event.perf_time, prev_time))
        if event.time < t0+epsilon:
            # event is before start of PFT
            prev_time = event.time
            prev_perf = event.perf_time
            prev_perf_adj = event.perf_time
            if debug: print('   before start of PFT, skipping')
            continue
        if pred:
            if event.kind == event_kind_note:
                if not pred(event.obj):
                    if debug: print('   not selected')
                    continue
            else:
                continue
        if event.obj.time > pft_end+epsilon:
            if debug: print('   note starts after PFT; skipping')
            continue
        if event.time - prev_time < epsilon:
            if debug:
                print('   same score time as prev; set perf time to %f'%prev_perf_adj)
            event.perf_time = prev_perf_adj
            continue

        # loop over PFT primitives up to the last one whose domain includes this event
        # precondition: event.time is not strictly before current seg
        while True:
            if debug: print('   event.time', event.time, 'seg_start', seg_start, ' seg_end', seg_end)
            use_this_seg = False
            if event.time < seg_end - epsilon:
                if debug: print('   strictly in seg; using it')
                use_this_seg = True
            elif event.time < seg_end + epsilon:
                next_seg = pft[seg_ind+1]
                if debug: print('   event at end of seg. next_seg.dt', next_seg.dt)
                if next_seg.dt > 0:  
                    use_this_seg = True
                else:
                    if debug: print('   next_seg.after', next_seg.after)
                    if next_seg.after:
                        use_this_seg = True
 
            if use_this_seg:
                if debug:
                    print('   using this seg')
                    print('   previous event: score time %f perf %f adjusted perf %f PFT integral %f'%(
                        prev_time, prev_perf, prev_perf_adj, prev_integral
                    ))
                if seg.dt == 0:
                    # Dirac delta case
                    if seg.after:
                        if debug: print('delta after')
                        prev_time = event.time
                        break
                    if debug: print('delta before')
                    # fall through, move to next seg
                else:
                    i = seg_integral + seg.integral(event.time - seg_start)
                        # integral of pft at this point
                    d = i - prev_integral
                        # integral since previous event
                    avg = scale_factor*d/(event.time - prev_time)
                        # average tempo since prev event
                    dperf = event.perf_time - prev_perf
                    prev_perf = event.perf_time
                    new_perf = prev_perf_adj + dperf*avg
                    event.perf_time = new_perf
                    prev_perf_adj = event.perf_time
                    prev_integral = i
                    if debug:
                        print('   new PFT integral %f; int since prev event %f; score time dt %f; int avg %f'%(
                            i, d, event.time-prev_time, avg
                        ))
                        print('   changed perf delay from %f to %f'%(
                            dperf, dperf*avg
                        ))
                    prev_time = event.time
                    break

            seg_start += seg.dt
            seg_integral += seg.integral_total()
            if debug: print('   moving to next seg')
            seg_ind += 1
            seg = pft[seg_ind]
            if debug:
                print('   next segment; dt %f int %f'%(seg.dt, seg.integral_total()))
            seg_end = seg_start + seg.dt
        # end loop over PFT segments
    # end loop over events
    self.transfer_start_end_events()

# change dur of notes starting between t0 and t1 so they end at t1
# (like a local sustain pedal)
def sustain(self, t0, t1, pred):
    for n in self.notes:
        if n.time<t0-epsilon:
            continue
        if n.time > t1:
            break
        if pred and not pred(n):
            continue
        end = n.time + n.dur
        if end < t1:
            n.dur = t1 - n.time

def pause_before(self, t, dt):
    for note in self.notes:
        if note.time + note.dur < t-epsilon:
            continue
        if note.time < t-epsilon:
            note.perf_dur += dt
        else:
            note.perf_time += dt
            note.perf_dur += dt

def pause_after(self, t, dt):
    for note in self.notes:
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

def roll(self, t, offsets, is_up=True, is_delay=False, pred=None, verbose=False):
    chord = []   # the notes at time t
    rolled = False
    for note in self.notes:
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

def t_adjust_list(self, offsets, pred):
    ind = 0
    for note in self.notes:
        if ind == len(offsets): break
        if pred(note):
            note.perf_time += offsets[ind]
            ind += 1

def t_adjust_notes(self, offset, pred):
    for note in self.notes:
        if pred(note):
            note.perf_time += offset

def t_adjust_func(self, func, pred):
    for note in self.notes:
        if pred(note):
            note.perf_time += func(note)

# perturb start time, and adjust duration to keep end time the same
# Possible TODO: adjust durations of earlier notes that end at this time
#
def t_random_uniform(self, min, max, pred=None):
    for note in self.notes:
        if pred and not pred(note): continue
        x = random.uniform(min, max)
        note.perf_time += x
        note.perf_dur -= x

def t_random_normal(self, stddev, max_sigma, pred=None):
    for note in self.notes:
        if pred and not pred(note): continue
        while True:
            x = numpy.random.normal()
            if abs(x) < max_sigma: break
        y = stddev*x
        note.perf_time += y
        note.perf_dur -= y
                
# --------------- Articulation ----------------------

def score_dur_abs(self, dur, pred):
    for note in self.notes:
        if pred(note):
            note.dur = dur

def score_dur_rel(self, factor, pred):
    for note in self.notes:
        if pred(note):
            note.dur *= factor

def score_dur_func(self, func, pred):
    for note in self.notes:
        if pred(note):
            note.dur = func(note)
            
def perf_dur_abs(self, dur, pred):
    for note in self.notes:
        if pred(note):
            note.perf_dur = dur

def perf_dur_rel(self, factor, pred):
    for note in self.notes:
        if pred(note):
            note.perf_dur *= factor

def perf_dur_func(self, func, pred):
    for note in self.notes:
        if pred(note):
            note.perf_dur = func(note)

# adjust articulation with a PFT
def perf_dur_pft(self, pft, t0, pred=None, rel=True):
    pft_check_closure(pft)
    seg_ind = 0
    seg = pft[0]
        # which segment we're on
    seg_start = t0
        # start time of that segment
    seg_end = t0 + seg.dt
    t_end = t0 + pft_dur(pft)
        # end time of function
    for n in self.notes:
        if n.time > t_end + epsilon:
            break
        if n.time < t0 - epsilon:
            continue
        if pred and not pred(n):
            continue
        while True:
            # skip segments as needed
            if n.time < seg_end - epsilon:
                v = seg.val(n.time - seg_start)
                break
            if n.time < seg_end + epsilon:
                # note is at end of this seg
                if seg.closed_end:
                    v = seg.y1
                    break
                if seg_ind == len(pft)-1:
                    return
            # move to next seg
            seg_start += seg.dt
            seg_ind += 1
            seg = pft[seg_ind]
            seg_end = seg_start + seg.dt
        # v is the adjustment factor
        if rel:
            n.perf_dur *= v
        else:
            n.perf_dur = v
        
# ----------- spatialization ----------------

# write a "position file": per-sample position -1..1,
# based on a PFT defining position as a function of score time.
def write_pos_file(self, pos_pft, fname, framerate):
    self.make_start_end_events()
    last_time = 0
    last_perf_time = 0
    events = []
    # events are sorted by score time
    for event in self.start_end:
        if event.time <= last_time:
            continue
        if event.perf_time <= last_perf_time:
            continue
        events.append(event)
        last_time = event.time
        last_perf_time = event.perf_time

    f = open(fname, 'w')
    pft_val = pft.pft_value(pos_pft)
    event_ind = 0
    ev0 = events[0]
    ev1 = events[1]
    slope = (ev1.time - ev0.time)/(ev1.perf_time - ev0.perf_time)
    for i in range(int(last_perf_time*framerate)):
        pt = i/framerate
        while pt > ev1.perf_time:
            event_ind += 1
            ev0 = events[event_ind]
            ev1 = events[event_ind+1]
            slope = (ev1.time - ev0.time)/(ev1.perf_time - ev0.perf_time)
        t = ev0.time + (pt-ev0.perf_time)*slope
        pos = pft_val.value(t)
        f.write("%f\n"%pos)
    f.close()

