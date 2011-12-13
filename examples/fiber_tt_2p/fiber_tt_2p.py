#-------------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Sep 8, 2011 by: rch

from enthought.traits.api import implements, Str
from core import \
    SPIRRID, Heaviside, RV, RF, IRF, SPIRRIDLAB
import numpy as np
from scipy.special import erf
import math

if __name__ == '__main__':

    # discretize the control variable (x-axis)
    e_arr = np.linspace(0, 2.0, 1000)

    #===========================================================================
    # Response function
    #===========================================================================
    class fiber_tt_2p(RF):
        '''Linear elastic, brittle filament.
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

        c_code = '''
                // Computation of the q( ... ) function
                if ( eps < 0 || eps > xi ){
                    q = 0.0;
                }else{
                      q = la * eps;
                }
                '''

    m_la, std_la = 10., 1.0
    m_xi, std_xi = 1.0, 0.1

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q = fiber_tt_2p(),
                e_arr = e_arr,
                n_int = 10,
                tvars = dict(la = RV('norm', m_la, std_la),
                             xi = RV('norm', m_xi, std_xi)
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
    slab = SPIRRIDLAB(s = s, save_output = True, show_output = True,
                      exact_arr = mu_q_ex(e_arr, m_xi, std_xi, m_la))

    #===========================================================================
    # Compare efficiency of sampling types 
    #===========================================================================
    powers = np.linspace(1, math.log(1000, 10), 10)
    n_int_range = np.array(np.power(10, powers), dtype = int)

#    slab.sampling_efficiency(n_int_range = n_int_range)

    #===========================================================================
    # Compare the structure of sampling
    #===========================================================================

#    slab.sampling_structure(ylim = 18.0, xlim = 1.2,)

    #===========================================================================
    # Compare the language efficiency
    #===========================================================================
#    e_arr = np.linspace(0, 2.0, 80)
#    s.set(e_arr = e_arr, n_int = 400)
    slab.set(n_recalc = 2, exact_arr = mu_q_ex(e_arr, m_xi, std_xi, m_la))
    slab.codegen_language_efficiency(extra_compiler_args = False)
#    slab.codegen_language_efficiency(extra_compiler_args = True)

