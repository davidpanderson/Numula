import numula.nscore as nscore
import numula.nuance as nuance
import numula.pianoteq as pianoteq
import matplotlib.pyplot as plot

# plot an exponential curve and its integral
#
def draw_curve(curvature, y0, y1, dt):
    e = nuance.ExpCurve(curvature, y0, y1, dt)
    n = 100
    x = [0]*n
    y = [0]*n
    yint = [0]*n
    for i in range(n):
        t = dt*i/n
        x[i] = t
        y[i] = e.val(t)
        yint[i] = e.integral(t)
    plot.rcParams['figure.figsize'] = (6,4)
    plot.suptitle('Curvature = %d'%curvature)
    plot.plot(x, y)
    #plot.plot(x, yint)
    plot.show()

#draw_curve(5, 1, 4, 10)
   
def exp_tempo(curvature):
    ns = nscore.Score(tempo=30)
    for i in range(64):
        p = 60 + (i*7)%12
        ns.insert_note(nscore.Note(i/64, 1/64, p, .5))
    ns.tempo_adjust_pft(
        [
            nuance.ExpCurve(curvature, 40, 80, 1)
        ]
    )
    ns.write_midi('data/exp_tempo_%d.midi'%curvature)
    pianoteq.play('data/exp_tempo_%d.midi'%curvature)
    pianoteq.midi_to_wav(
        'data/exp_tempo_%d.midi'%curvature,
        'data/exp_tempo_%d.wav'%curvature
    )

#exp_tempo(-5)
#exp_tempo(-2)
exp_tempo(0)
#exp_tempo(2)
#exp_tempo(5)

def exp_vol(curvature):
    ns = nscore.Score(tempo=30)
    for i in range(64):
        p = 60 + (i*7)%12
        ns.insert_note(note.Note(i/64, 1/64, p, .5))
    ns.vol_adjust_pft(
        [
            nuance.ExpCurve(curvature, .2, 1.9, 1)
        ]
    )
    ns.write_midi('data/exp_vol_%d.midi'%curvature)
    #pianoteq.play('data/exp_vol_%d.midi'%curvature)
    pianoteq.midi_to_wav(
        'data/exp_vol_%d.midi'%curvature,
        'data/exp_vol_%d.wav'%curvature
    )

#exp_vol(-5)
#exp_vol(-2)
#exp_vol(0)
#exp_vol(2)
#exp_vol(5)
