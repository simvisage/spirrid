#-------------------------------------------------------------------------------
#
# Copyright (c) 2012
# IMB, RWTH Aachen University,
# ISM, Brno University of Technology
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in the Spirrid top directory "licence.txt" and may be
# redistributed only under the conditions described in the aforementioned
# license.
#
# Thanks for using Simvisage open source!
#
#-------------------------------------------------------------------------------

from etsproxy.traits.api import implements, Str
from scipy.special import erf
from spirrid import SPIRRID, Heaviside, RV, RF, IRF
from spirrid.extras.error_eval import ErrorEval
import math
import numpy as np
import pylab as p
import multiprocessing
import time

#===========================================================================
# Response function
#===========================================================================
class fiber_tt_2p(RF):
    ur'''
Response Function with two-parameters.
======================================
    
The function describes a linear dependency with a coefficient :math:`\lambda` 
up to the threshold :math:`\xi` and zero value beyond the threshold: 
    
..    math::
       q( \varepsilon; \theta, \lambda ) = \lambda \varepsilon H( \xi - \varepsilon )

where the variables :math:`\lambda=` stiffness parameter and :math:`\xi=` 
breaking strain are considered random and normally distributed. The function 
:math:`H(\eta)` represents the Heaviside function with values 0 for 
:math:`\eta < 0` and 1 for :math:`\eta > 0`.
   
    '''
    implements(IRF)

    title = Str('brittle filament')

    def __call__(self, e, la, xi):
        ''' Response function of a single fiber '''
        return la * e * Heaviside(xi - e)

    cython_code = '''
            # Computation of the q( ... ) function
            if eps < 0 or eps > xi:
                q = 0.0
            else:
                q = la * eps
            '''

    weave_code = '''
            // Computation of the q( ... ) function
            if ( eps < 0 || eps > xi ){
                q = 0.0;
            }else{
                  q = la * eps;
            }
            '''


m_la, std_la = 10., 1.0
m_xi, std_xi = 1.0, 0.1

# discretize the control variable (x-axis)
e_arr = np.linspace(0, 2.0, 80)

#===========================================================================
# Exact solution
#===========================================================================
def mu_q_ex(e, m_xi, std_xi, m_la):
    return e * (0.5 - 0.5 *
                erf(0.5 * math.sqrt(2) * (e - m_xi) / std_xi)) * m_la

#===========================================================================
# Randomization
#===========================================================================
s = SPIRRID(q = fiber_tt_2p(),
        e_arr = e_arr,
        n_int = 10,
        tvars = dict(la = RV('norm', m_la, std_la),
                     xi = RV('norm', m_xi, std_xi)
                     ),
        codegen_type = 'numpy',
        sampling_type = 'MCS'
        )

def run(a):

    s.recalc = True

    return s.mu_q_arr


def sum_arr(arr):
    return

count = np.zeros(80)

def cb(r):
    global count
    print r[0][10]
    count = count + r[0]

if __name__ == '__main__':


    exact_arr = mu_q_ex(e_arr, m_xi, std_xi, m_la)

    mu_q_arr_sum = []
    n_streams = 1000

    start = time.time()

    #pool = multiprocessing.Pool(processes = 4)
    pool = multiprocessing.Pool(None)

    tasks = range(n_streams)

    r = pool.map_async(run, tasks, callback = mu_q_arr_sum.append)# cb)
    r.wait()

    mu_q = np.array(mu_q_arr_sum).sum(axis = 1).T / float(n_streams)#count.T
    p.plot(e_arr, mu_q, 'k-')
    p.plot(e_arr, exact_arr, 'r-')

    err = ErrorEval(exact_arr = exact_arr)
    print 'error', err.eval_error_all(mu_q.T)

    print 'time', time.time() - start

    p.show()




