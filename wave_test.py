import wave, struct

obj = wave.open('nocturne.wav')
print( "Number of channels",obj.getnchannels())
print ( "Sample width",obj.getsampwidth())
print ( "Frame rate.",obj.getframerate())
print ("Number of frames",obj.getnframes())
print ( "parameters:",obj.getparams())

x = obj.readframes(1024)
obj.close()
print(len(x))
y = struct.unpack("2048h", x)
y1 = [0]*1024
y2 = [0]*1024
for i in range(1024):
    y1[i] = y[i*2]
    y2[i] = y[i*2+1]

import matplotlib.pyplot as plot

plot.plot(range(1024), y1, label='L')
plot.plot(range(1024), y2, label='R')
plot.show()



