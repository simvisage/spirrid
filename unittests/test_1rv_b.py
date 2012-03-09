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
import numpy as np
import pylab as p

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

def run():

    m_la, std_la = 10., 1.0
    m_xi, std_xi = 1.0, 0.1

    # discretize the control variable (x-axis)
    e_arr = np.linspace(0, 2.0, 80)

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q = fiber_tt_2p(),
                e_arr = e_arr,
                n_int = 10,
                tvars = dict(la = RV('norm', m_la, std_la),
                             xi = m_xi, #RV('norm', m_xi, std_xi)
                             ),
                sampling_type = 'TGrid',
                codegen_type = 'numpy',
                )

    p.plot(e_arr, s.mu_q_arr, 'b-x')

    s.codegen_type = 'weave'

    p.plot(e_arr, s.mu_q_arr, 'r-')

    p.show()

if __name__ == '__main__':
    run()

