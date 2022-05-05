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

import numpy, random
from note import *

class linear:
    def __init__(self, y0, y1, dt, closed_start=True, closed_end=True):
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

# duration of a PFT
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

# adjust tempo of selected notes.
# pft is tempo function defined from (score) t0  to t1.
# Its value is in units of beats per minute
# (60 = no change, 120 = speed by 2X)
# conceptually, F is 60 outside this interval
#
# - compute the NoteSet's sorted list of start/end "events",
#   each with (score) time and a perf time.
# - for each successive pair of events, compute average of PFT
#   for the score time interval; scale perf time interval by this.
# - update the (perf) time and dur of the corresponding Note and Pedal objects.
#
# if "normalize", scale F so that its average is 1.
#
def tempo_adjust_pft(self, pft, t0=0, pred=None, normalize=False):
    pft_bpm(pft)    # convert to inverse tempo function
    self.make_start_end_events()
    seg_ind = 0
    seg = pft[0]
    seg_start = t0
    seg_end = t0 + seg.dt
    pft_end = t0 + pft_dur(pft)
    seg_integral = 0
        # integral up to current seg
    debug = False

    scale_factor = 1
    if normalize:
        scale_factor = 1/pft_avg(pft)
        if debug: print('scale factor: ', scale_factor)

    # loop over events.
    # keep track of params of previous event
    #
    prev_time = 0    # its score time
    prev_perf = 0     # its perf time
    prev_perf_adj = 0   # its adjusted perf time
    prev_integral = 0    # integral of pft at that point
    for event in self.start_end:
        if debug: print('event time %f'%event.time)
        if event.time < t0+epsilon:
            prev_time = event.time
            prev_perf = event.perf_time
            prev_perf_adj = event.perf_time
            continue
        if pred:
            if event.kind == event_kind_note:
                if not pred(event.obj):
                    continue
            else:
                continue
        if event.time - prev_time < epsilon:
            event.perf_time = prev_perf_adj
            continue
        while True:
            if event.time < seg_end + epsilon:
                if debug:
                    print('prev_time %f pref_perf %f prev_perf_adj %f prev_integral %f'%(
                        prev_time, prev_perf, prev_perf_adj, prev_integral
                    ))  
                i = seg_integral + seg.integral(event.time - seg_start)
                    # integral of pft at this point
                d = i - prev_integral
                    # integral since previous event
                avg = scale_factor*d/(event.time - prev_time)
                    # average tempo since prev event
                dperf = event.perf_time - prev_perf
                prev_perf = event.perf_time
                event.perf_time = prev_perf_adj + dperf*avg
                prev_perf_adj = event.perf_time
                prev_integral = i
                prev_time = event.time
                if debug:
                    print('time %f i %f d %f avg %f dperf %f perf_adj %f'%(
                        event.time, i, d, avg, dperf, prev_perf_adj
                    ))
                break
            else:
                if debug: print('moving to next segment')
                seg_start  += seg.dt
                seg_integral += seg.integral_total()
                seg_ind += 1
                if seg_ind == len(pft):
                    if debug: print('end of PFT')
                    break
                seg = pft[seg_ind]
                seg_end = seg_start + seg.dt
        if seg_ind == len(pft):
            break
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


