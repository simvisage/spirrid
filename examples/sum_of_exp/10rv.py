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
from spirrid.extras import SPIRRIDLAB
import math
import numpy as np

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

    def __call__(self, e, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10):
        ''' Response function of a single fiber '''
        return np.exp(-x1 ** 2) + np.exp(-x2 ** 2) + np.exp(-x3 ** 2) + \
            np.exp(-x4 ** 2) + np.exp(-x5 ** 2) + np.exp(-x6 ** 2) + \
            np.exp(-x7 ** 2) + np.exp(-x8 ** 2) + np.exp(-x9 ** 2) + \
            np.exp(-x10 ** 2)

    cython_code = '''
            # Computation of the q( ... ) function
            if eps < 0 or eps > xi:
                q = 0.0
            else:
                q = la * eps
            '''

    weave_code = '''
            q = exp(-pow(x1,2.)) + exp(-pow(x2,2.)) + exp(-pow(x3,2.)) + exp(-pow(x4,2.)) + exp(-pow(x5,2.)) +
                exp(-pow(x6,2.)) + exp(-pow(x7,2.)) + exp(-pow(x8,2.)) + exp(-pow(x9,2.)) + exp(-pow(x10,2.));
            '''

def create_demo_object(fig_output_dir='fig'):

    # discretize the control variable (x-axis)
    e_arr = np.array([1.0])#np.linspace(0, 2.0, 80)

    # n_int range for sampling efficiency test
    #powers = np.linspace(1, math.log(5, 9), 5)
    n_int_range = np.arange(4, 8, 1, dtype=int)#np.array(np.power(10, powers), dtype=int)

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=fiber_tt_2p(),
                sampling_type='PGrid',
                codegen_type='weave',
                e_arr=e_arr,
                n_int=10,
                tvars=dict(x1=RV('norm', 0., 1.),
                           x2=RV('norm', 0., 1.),
                           x3=RV('norm', 0., 1.),
                           x4=RV('norm', 0., 1.),
                           x5=RV('norm', 0., 1.),
                           x6=RV('norm', 0., 1.),
                           x7=RV('norm', 0., 1.),
                           x8=RV('norm', 0., 1.),
                           x9=RV('norm', 0., 1.),
                           x10=RV('norm', 0., 1.),
                             ),
                )
    print 'mu', s.mu_q_arr / 10.

    #===========================================================================
    # Exact solution
    #===========================================================================
    def mu_q_ex():
        return np.array([10 * np.sqrt(3) / 3.])

    #===========================================================================
    # Lab
    #===========================================================================
    slab = SPIRRIDLAB(s=s, save_output=False, show_output=True,
                      dpi=300,
                      fig_output_dir=fig_output_dir,
                      plot_mode='subplots',
                      exact_arr=mu_q_ex(),
                      n_int_range=n_int_range,
                      extra_compiler_args=True,
                      le_sampling_lst=['LHS', 'PGrid'],
                      le_n_int_lst=[5, 10])

    return slab

if __name__ == '__main__':

    slab = create_demo_object()

    slab.configure_traits()
