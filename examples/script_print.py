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
from fiber_tt_2p.fiber_tt_2p import fiber_tt_2p
import numpy as np
import math
from spirrid import SPIRRID, Heaviside, RV, RF, IRF

def demo():

    m_la, std_la = 10., 1.0
    m_xi, std_xi = 1.0, 0.1

    # discretize the control variable (x-axis)
    e_arr = np.linspace(0, 2.0, 80)

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=fiber_tt_2p(),
                sampling_type='TGrid',
                codegen_type='weave',
                e_arr=e_arr,
                n_int=10,
                theta_vars=dict(la=RV('norm', m_la, std_la),
                                xi=RV('norm', m_xi, std_xi)
                                ),
                )

    #print current configuration of the integrator
    #print s.__str__()

    # print code of the weave (or cython) implementation
    print s.codegen.code

if __name__ == '__main__':

    demo()
