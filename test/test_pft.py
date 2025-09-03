
def test_obj():
    p = [
        PFTObject(1, [1,2]),
        PFTObject(3, [4,5])
    ]
    pv = PFTValue(p)
    t = 0
    while not pv.ended:
        print(t, pv.value(t))
        t += .25
#test_obj()

# test PFT primitives
def test_prim():
    p = Linear(1, 2, 1)
    print('linear')
    for i in range(11):
        x = i/10.
        print('val %.3f int %.3f inv %.3f'%(p.val(x), p.integral(x), p.integral_inverse(x)))
    c = -0.01
    p = ExpCurve(c, 1, 2, 1)
    print('exponential, curvature', c)
    for i in range(11):
        x = i/10.
        inv = p.integral_inverse(x)
        print('val %.3f int %.3f inv %.3f'%(p.val(x), p.integral(x), inv))
        #print('val %.3f int %.3f'%(p.val(x), p.integral(x)))

test_prim()
