import mido
import note

def read_midifile(file):
    mf = mido.MidiFile(file)
    ns = note.NoteSet()
    for i, track in enumerate(mf.tracks):
        t = 0
        notes = [None]*128
        for msg in track:
            if msg.type == 'note_on':
                print(msg)
                t += msg.time/3840
                pitch = msg.note
                if notes[pitch]:
                    # overlap case.  End current note at this pitch, and start a new one
                    n = notes[pitch]
                    n.dur = t-n.time
                    ns.insert_note(n)
                    n.time = t
                    n.velocity = msg.velocity/128
                else:
                    n = note.Note(t, 0, pitch, msg.velocity/128)
                    notes[pitch] = n
            elif msg.type == 'note_off':
                print(msg)
                t += msg.time/3840
                pitch = msg.note
                if not notes[pitch]:
                    # this happens in overlap case
                    continue
                n = notes[pitch]
                notes[pitch] = None
                n.dur = t-n.time
                ns.insert_note(n)
    ns.done()
    ns.print()
    ns.write_midi('test_out.midi')
    
def test(file):
    mid = mido.MidiFile(file)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)

test('cryptogram.mid')
#read_midifile('cryptogram.mid')
