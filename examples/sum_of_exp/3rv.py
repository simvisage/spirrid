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
class RV2(RF):
    ur'''
   
    '''
    implements(IRF)

    title = Str('brittle filament')

    def __call__(self, e, x1, x2, x3):
        ''' Response function of a single fiber '''
        return np.exp(-x1 ** 2) + np.exp(-x2 ** 2) + np.exp(-x3 ** 2)

    cython_code = '''
                q = np.exp(-x1*x1) + np.exp(-x2*x2) + np.exp(-x3*x3)
            '''

    weave_code = '''{
                  q = exp(-x1*x1) + exp(-x2*x2);
                  //printf("%100f\\n",q);
            }
            '''

def create_demo_object(fig_output_dir='fig'):

    # discretize the control variable (x-axis)
    e_arr = np.array([1.0])#np.linspace(0, 2.0, 80)

    # n_int range for sampling efficiency test
    powers = np.linspace(1, math.log(40, 10), 50)
    n_int_range = np.array(np.power(10, powers), dtype=int)
    #n_int_range = np.array([10, 100, 200, 300, 400, 500, 800, 1000, 1500, 2000])

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=RV2(),
                e_arr=e_arr,
                n_int=100,
                tvars=dict(x1=RV('norm', 0, 1),
                           x2=RV('norm', 0, 1),
                           x3=RV('norm', 0, 1)
                             ),
                #codegen_type='weave',
                sampling_type='TGrid'
                )
    from decimal import Decimal
    print Decimal((s.mu_q_arr / 3.)[0])

    #===========================================================================
    # Exact solution
    #===========================================================================
    def mu_q_ex():
        return np.array([3 * np.sqrt(3) / 3.])

    print Decimal((s.mu_q_arr - mu_q_ex())[0])

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
                      le_n_int_lst=[440, 5000])

    return slab

if __name__ == '__main__':

    slab = create_demo_object()

    slab.configure_traits()
