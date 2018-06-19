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

def create_demo_object(fig_output_dir='fig'):

    m_la, std_la = 10., 1.0
    m_xi, std_xi = 1.0, 0.1

    # discretize the control variable (x-axis)
    e_arr = np.linspace(0, 2.0, 80)

    # n_int range for sampling efficiency test
    powers = np.linspace(1, math.log(500, 10), 50)
    n_int_range = np.array(np.power(10, powers), dtype=int)

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=fiber_tt_2p(),
                sampling_type='TGrid',
                codegen_type='cython',
                e_arr=e_arr,
                n_int=10,
                theta_vars=dict(la=RV('norm', m_la, std_la),
                             xi=RV('norm', m_xi, std_xi)
                             ),
                )

    #===========================================================================
    # Exact solution
    #===========================================================================
    def mu_q_ex(e, m_xi, std_xi, m_la):
        return e * (0.5 - 0.5 *
                    erf(0.5 * math.sqrt(2) * (e - m_xi) / std_xi)) * m_la

    #===========================================================================
    # Lab
    #===========================================================================
    slab = SPIRRIDLAB(s=s, save_output=False, show_output=True,
                      dpi=300,
                      fig_output_dir=fig_output_dir,
                      exact_arr=mu_q_ex(e_arr, m_xi, std_xi, m_la),
                      plot_mode='subplots',
                      n_int_range=n_int_range,
                      extra_compiler_args=True,
                      le_sampling_lst=['LHS', 'PGrid'],
                      le_n_int_lst=[440, 5000])

    return slab

if __name__ == '__main__':

    slab = create_demo_object()

    slab.configure_traits()
