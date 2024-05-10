import random

last = 0

def brown():
    global last
    x = random.random()-.5
    last += x
    last *= .9
    return last

for i in range(1000):
    print(brown())
