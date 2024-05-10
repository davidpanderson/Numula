import numula.pianoteq_rpc as pianoteq_rpc
import time

def test_rpc():
    all_presets = pianoteq_rpc.rpc("getListOfPresets")["result"]
    print(all_presets)

#test_rpc()

def test_file():
    ret = pianoteq_rpc.loadMidiFile('data/wasserklavier.midi')
    print(ret)
    for i in range(2):
        ret = pianoteq_rpc.midiSeek(30)
        print(ret)
        ret = pianoteq_rpc.midiPlay()
        print(ret)
        time.sleep(5)
        pianoteq_rpc.midiStop()
        
test_file()

#print(pianoteq_rpc.midiPlay())

