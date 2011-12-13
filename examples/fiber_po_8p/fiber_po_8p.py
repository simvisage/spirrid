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
    SPIRRID, RV
from core import SPIRRIDLAB
import numpy as np
import math
from quaducom.pullout.constant_friction_finite_fiber import \
    ConstantFrictionFiniteFiber

if __name__ == '__main__':

    #===========================================================================
    # Control variable
    #===========================================================================
    e_arr = np.linspace(0, 0.012, 80)

    #===========================================================================
    # Randomization
    #===========================================================================
    tvars = dict(fu = RV('weibull_min', 1200.0e6, 200.),
                  qf = 1500.0,
                  # qf = RV('uniform', 1500., 100.),
                  L = 0.02, # 
                  # L = RV('uniform', 0.02, 0.02 / 2.),
                  A = RV('norm', 5.30929158457e-10, .03 * 5.30929158457e-10),
                  E_mod = RV('uniform', 70.e9, 250.e9),
                  z = RV('uniform', 0.0, 0.03),
                  phi = 0.0, # 
                  # phi = RV('cos_distr', 0.0, 1.0),
                  # phi = RV('uniform', 0.0, 1.0),
                  f = RV('uniform', 0.0, 0.03))

    #===========================================================================
    # Integrator object
    #===========================================================================
    s = SPIRRID(q = ConstantFrictionFiniteFiber(),
                e_arr = e_arr,
                n_int = 30,
                tvars = tvars,
                )

    #===========================================================================
    # Lab
    #===========================================================================
    slab = SPIRRIDLAB(s = s, save_output = True, show_output = True,
                      qname = 'fiber_po_8p',
                      )

    #===========================================================================
    # Compare efficiency of sampling types 
    #===========================================================================
    powers = np.linspace(1, math.log(20, 10), 6)
    n_int_range = np.array(np.power(10, powers), dtype = int)
    #slab.sampling_efficiency(n_int_range = n_int_range)

    #===========================================================================
    # Compare the structure of sampling
    #===========================================================================

    #slab.sampling_structure(ylim = 10.0, xlim = 0.012, plot_idx = [0, 3])

    #===========================================================================
    # Compare the code efficiency
    #===========================================================================

    s.sampling_type = 'TGrid'
    slab.codegen_efficiency()

