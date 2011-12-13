'''
Created on Oct 31, 2011

@author: kelidas
'''

# test masked array efficiency
import numpy as np

import platform
if platform.system() == 'Linux':
    from time import time as sysclock
elif platform.system() == 'Windows':
    from time import clock as sysclock

def H(x):
    return x > 0

a = np.linspace(0, 1, 5000)[:, None]
b = np.linspace(0, 1, 5000)[None, :]
a_m = np.ma.array(a, mask = a > 0.5)
b_m = np.ma.array(b, mask = b > 0.5)

def f(a, b):
    return a * b * np.cos(a) * np.sin(b)

def f_H(a, b):
    return a * b * np.cos(a) * np.sin(b) * H(0.5 - a)

def f_m(a, b):
    return a * b * np.ma.cos(a) * np.ma.sin(b)

start = sysclock()
res = f(a, b)
print sysclock() - start, 'full array'
del res

start = sysclock()
res = f_H(a, b)
print sysclock() - start, 'heaviside'
del res

start = sysclock()
res = f(a, b) * H(0.5 - a)
print sysclock() - start, 'heaviside, alt 2'
del res

start = sysclock()
res = f(a_m, b_m)
print sysclock() - start, 'masked array, numpy function'
del res

start = sysclock()
res = f_m(a_m, b_m)
print sysclock() - start, 'masked array, mask function'
del res








