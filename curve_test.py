import note, nuance, pianoteq
import matplotlib.pyplot as plot

# plot an exponential curve and its integral
#
def draw_curve(curvature, y0, y1, dt):
    e = nuance.exp_curve(curvature, y0, y1, dt)
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
    plot.plot(x, y)
    #plot.plot(x, yint)
    plot.show()

draw_curve(-5, 1, 4, 10)
   
def exp_tempo(curvature):
    ns = note.NoteSet()
    for i in range(64):
        ns.insert_note(note.Note(i/64, 1/64, 60, .5))
    ns.set_tempo(30)
    ns.done()
    ns.tempo_adjust_pft(
        [
            nuance.exp_curve(curvature, 40, 80, 1)
        ]
    )
    ns.write_midi('data/exp_tempo.midi')
    pianoteq.play('data/exp_tempo.midi')

#exp_tempo(-5)

def exp_vol(curvature):
    ns = note.NoteSet()
    for i in range(64):
        ns.insert_note(note.Note(i/64, 1/64, 60, .5))
    ns.set_tempo(30)
    ns.done()
    ns.tempo_adjust_vol(
        [
            nuance.exp_curve(curvature, .5, 1.5, 1)
        ]
    )
    ns.write_midi('data/exp_vol.midi')
    pianoteq.play('data/exp_vol.midi')
