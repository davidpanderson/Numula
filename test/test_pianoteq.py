import numula_path
import numula.pianoteq as pianoteq
import time

def test_rpc():
    all_presets = pianoteq.rpc("getListOfPresets")["result"]
    with open('presets.json', 'w') as f:
        print(all_presets, file=f)

#test_rpc()

def test_preset():
    ret = pianoteq.loadPreset('NY Steinway D Classical (for wasser)', 'My Presets')
#test_preset()

def test_file():
    ret = pianoteq.loadMidiFile('data/wasserklavier.midi')
    print(ret)
    for i in range(2):
        ret = pianoteq.midiSeek(30)
        ret = pianoteq.midiPlay()
        time.sleep(5)
        pianoteq.midiStop()
        
test_file()

#print(pianoteq.midiPlay())

def preset_test():
    pianoteq.play_midi_file('data/scale.midi', preset='C. Grimaldi Harpsichord A')
    #pianoteq.midi_to_wav('data/scale.midi', 'data/scale.wav', preset='Celesta Tremo')
#preset_test()
