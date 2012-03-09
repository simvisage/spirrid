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
from spirrid import SPIRRID, RV, RF, IRF, Heaviside
import numexpr as ne
import numpy as np
import pylab as p

def Heaviside_ne(x):
    ''' Heaviside function '''
    return ne.evaluate("x >= 0")#( np.sign( x ) + 1.0 ) / 2.0


def main():

    #===========================================================================
    # Response function
    #===========================================================================
    class fiber_tt_5p_np(RF):
        ''' Response function of a single fiber '''
        implements(IRF)

        title = Str('brittle filament')

        def __call__(self, eps, lambd, xi, E_mod, theta, A):
            '''
            Implements the response function with arrays as variables.
            first extract the variable discretizations from the orthogonal grid.
            '''
            eps_ = (eps - theta * (1 + lambd)) / ((1 + theta) * (1 + lambd))

            eps_ *= Heaviside(eps_)
            eps_grid = eps_ * Heaviside(xi - eps_)
            q_grid = E_mod * A * eps_grid

            return q_grid



    class fiber_tt_5p_ne(RF):
        ''' Response function of a single fiber '''
        implements(IRF)

        title = Str('brittle filament')

        def __call__(self, eps, lambd, xi, E_mod, theta, A):
            '''
            Implements the response function with arrays as variables.
            first extract the variable discretizations from the orthogonal grid.
            '''
            eps_ = ne.evaluate("((eps - theta * (1 + lambd)) / ((1 + theta) * (1 + lambd)))")
            tmp = Heaviside_ne(eps_)
            eps_ = ne.evaluate('eps_*tmp')
            tmp = Heaviside_ne(ne.evaluate("(xi - eps_)"))
            eps_grid = ne.evaluate("eps_ * tmp")
            q_grid = ne.evaluate("E_mod * A * eps_grid")

            return q_grid
            # all in one row, slower alternative
            #return ne.evaluate("E_mod * A *((eps - theta * (1 + lambd)) / ((1 + theta) * (1 + lambd))) * (((eps - theta * (1 + lambd)) / ((1 + theta) * (1 + lambd)))>=0) *  ((xi-((eps - theta * (1 + lambd)) / ((1 + theta) * (1 + lambd))))>=0)")



    # set the mean and standard deviation of the two random variables
    la_mean, la_stdev = 0.1, 0.02
    xi_mean, xi_stdev = 0.019027, 0.0022891
    E_mean, E_stdev = 70.0e+9, 15.0e+9
    th_mean, th_stdev = 0.005, 0.001
    A_mean, A_stdev = 5.3e-10, 1.0e-11

    # construct the normal distributions and get the methods
    # for the evaluation of the probability density functions
    g_la = RV('norm', la_mean, la_stdev)
    g_xi = RV('norm', xi_mean, xi_stdev)
    g_E = RV('norm', E_mean, E_stdev)
    g_th = RV('norm', th_mean, th_stdev)
    g_A = RV('norm', A_mean, A_stdev)


    # discretize the control variable (x-axis)
    e_arr = np.linspace(0, 0.04, 80)

    #===========================================================================
    # Randomization
    #===========================================================================


    s_ne = SPIRRID(q = fiber_tt_5p_ne(),
                e_arr = e_arr,
                n_int = 10,
                tvars = dict(lambd = g_la, xi = g_xi, E_mod = g_E, theta = g_th, A = g_A),
                )
    s_np = SPIRRID(q = fiber_tt_5p_np(),
                e_arr = e_arr,
                n_int = 10,
                tvars = dict(lambd = g_la, xi = g_xi, E_mod = g_E, theta = g_th, A = g_A),
                )

    print 'Evaluation using NumPy'
    print 'numpy time', s_np.exec_time
    print 'Evaluation using numexpr'
    print 'numexpr time', s_ne.exec_time

    p.plot(e_arr, s_np.mu_q_arr, label = 'numpy')
    p.plot(e_arr, s_ne.mu_q_arr, label = 'numexpr')
    p.legend()
    p.show()

if __name__ == '__main__':
    main()
