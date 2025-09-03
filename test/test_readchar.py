import readchar

def rctest():
    x = readchar.readchar()
    print(x)
rctest()

# character input test
# Note: this doesn't work when run from Idle.
# You need to run it from cmd or powershell: python.exe test.py
#
def input_test():
    while True:
        x = readchar.readkey()
        print('got ', x)
#input_test()
