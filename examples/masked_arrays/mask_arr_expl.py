'''
Created on Apr 10, 2012

@author: kelidas
'''

# test masked array efficiency
import numpy as np
import platform

if platform.system() == 'Linux':
    from time import time as sysclock
elif platform.system() == 'Windows':
    from time import clock as sysclock

def multip():

    a = np.linspace(0, 1, 100000)
    b = np.linspace(0, 1, 100000)
    a[a > 0.5] = 0
    b[b > 0.5] = 0
    a_m = np.ma.array(a, mask=a > 0.5)
    b_m = np.ma.array(b, mask=b > 0.5)

    res1a = a.copy()
    start = sysclock()
    res1a *= b
    print sysclock() - start, 'full array - res1a *= b'

    start = sysclock()
    res1b = a * b
    print sysclock() - start, 'full array - res1b = a * b'

    res2a = a_m.copy()
    start = sysclock()
    res2a *= b_m
    print sysclock() - start, 'numpy masked array - res2a *= b_m'

    start = sysclock()
    res2b = a_m * b_m
    print sysclock() - start, 'numpy masked array - res2b = a_m * b_m'

    res3 = a.copy()
    start = sysclock()
    res3[res3 > 0] *= b[res3 > 0]
    print sysclock() - start, 'mask explicit'

    print 'all arrays are equal -', np.array_equal(res1a, res1b) and np.array_equal(res2a.data, res2b.data)\
                                 and np.array_equal(res1a, res2a.data) and np.array_equal(res2b.data, res3)

def power():

    a = np.linspace(0, 1, 100000)
    a[a > 0.5] = 0
    a_m = np.ma.array(a, mask=a > 0.5)

    res1a = a.copy()
    start = sysclock()
    res1a **= 2
    print sysclock() - start, 'full array - res1a **= 2'

    start = sysclock()
    res1b = a ** 2
    print sysclock() - start, 'full array - res1b = a ** 2'

    res2a = a_m.copy()
    start = sysclock()
    res2a **= 2
    print sysclock() - start, 'numpy masked array - res2a **= 2'

    start = sysclock()
    res2b = a_m ** 2
    print sysclock() - start, 'numpy masked array - res2b = a_m ** 2'

    res3 = a.copy()
    start = sysclock()
    res3[res3 > 0] **= 2
    print sysclock() - start, 'mask explicit'

    print 'all arrays are equal -', np.array_equal(res1a, res1b) and np.array_equal(res2a.data, res2b.data)\
                                 and np.array_equal(res1a, res2a.data) and np.array_equal(res2b.data, res3)

if __name__ == '__main__':
    print '##### MULTIPLICATION'
    multip()
    print '##### POWER'
    power()






