import numula.pianoteq as pianoteq
import time

def test_rpc():
    all_presets = pianoteq.rpc("getListOfPresets")["result"]
    print(all_presets)

#test_rpc()

def test_file():
    ret = pianoteq.loadMidiFile('data/wasserklavier.midi')
    print(ret)
    for i in range(2):
        ret = pianoteq.midiSeek(30)
        print(ret)
        ret = pianoteq.midiPlay()
        print(ret)
        time.sleep(5)
        pianoteq.midiStop()
        
test_file()

#print(pianoteq.midiPlay())

