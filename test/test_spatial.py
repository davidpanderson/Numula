
# make some notes with different pitches and same vol
# (test input for panning)
# Also make a "pan position file"
def pan_test():
    ns = Score()
    for i in range(240):
        ns.append_note(Note(0, 1/16, random.randrange(48, 72), .5))
        ns.advance_time(1/16)
    ns.write_midi('data/pan_test.midi')
    pos_array = ns.get_pos_array(
        [
            Linear(-1, 1, 61/4)
        ], 44100
    )
    pianoteq.play_midi_file('data/pan_test.midi')

#pan_test()
