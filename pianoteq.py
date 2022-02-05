# play a MIDI file using pianoteq

import os

def play(file):
    cmd = '"c:/program files/modartt/pianoteq 7/pianoteq 7.exe"  --play --midi %s'%file
    os.system(cmd)
