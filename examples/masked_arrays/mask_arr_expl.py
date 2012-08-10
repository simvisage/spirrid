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

def Heaviside(x):
    ''' Heaviside function '''
    return x >= 0

def multip():

    a = np.linspace(0, 1, 1000000)
    b = np.linspace(0, 1, 1000000)
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

    start = sysclock()
    res4 = a * Heaviside(-a + 0.5) * b * Heaviside(-b + 0.5)
    print sysclock() - start, 'Heaviside'

    print 'all arrays are equal -', np.array_equal(res1a, res1b) and np.array_equal(res2a.data, res2b.data)\
                                 and np.array_equal(res1a, res2a.data) and np.array_equal(res2b.data, res3)\
                                 and np.array_equal(res4, res3)

def power():

    a = np.linspace(0, 1, 5)
    a0 = a.copy()
    par = 0.5
    mask = a > par
    a0[mask] = 0
    a_m = np.ma.array(a, mask=mask)

    res1a = a0.copy()
    start = sysclock()
    res1a **= 2
    print sysclock() - start, 'zeroed array, inplace, without logical operator (single pass) - res1a **= 2'

    start = sysclock()
    res1b = a0 ** 2
    print sysclock() - start, 'zeroed array, (single pass) allocation of additional array - res1b = a ** 2'

    res2a = a_m.copy()
    start = sysclock()
    res2a **= 2
    print sysclock() - start, 'implicit mask, inplace, access indirection through mask - res2a **= 2'

    start = sysclock()
    res2b = a_m ** 2
    print sysclock() - start, 'implicit mask, assigned, access indirection through mask - res2b = a_m ** 2'

    res3 = a.copy()
    start = sysclock()
    res3[a <= par] **= 2
    print sysclock() - start, 'explicit mask, inplace, two passes through array - res3[res3 > 0] **= 2'

    start = sysclock()
    res4 = (a * Heaviside(par - a)) ** 2
    print sysclock() - start, 'Heaviside, two passes - res4 = (a * Heaviside(-a + 0.5)) ** 2'

    print 'all arrays are equal -', (np.array_equal(res1a[~mask], res1b[~mask]) and
                                      np.array_equal(res2a.data[~mask], res2b.data[~mask]) and
                                      np.array_equal(res1a[~mask], res2a.data[~mask]) and
                                      np.array_equal(res2b.data[~mask], res3[~mask]) and
                                      np.array_equal(res4[~mask], res3[~mask]))

if __name__ == '__main__':
    print '##### MULTIPLICATION'
    multip()
    print '##### POWER'
    power()






