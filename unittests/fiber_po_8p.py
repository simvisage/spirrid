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

from spirrid import SPIRRID, RV, Heaviside
import math
import numpy as np
from etsproxy.traits.api import Float, Str, implements, Range
from math import pi, e
from numpy import  cos, sqrt, exp
from spirrid import IRF, RF

class ConstantFrictionFiniteFiber(RF):

    implements(IRF)

    title = Str('pull-out with constant friction')

    fu = Float(1200e6, auto_set = False, enter_set = True,
                distr = ['weibull_min'])

    qf = Float(1500., auto_set = False, enter_set = True,
                distr = ['uniform', 'norm'])

    L = Float(0.02, auto_set = False, enter_set = True,
               distr = ['uniform'])

    A = Float(5.30929158457e-10, auto_set = False, enter_set = True,
               distr = ['uniform', 'weibull_min'])

    E_mod = Float(70.0e9, auto_set = False, enter_set = True,
                   distr = ['uniform'])

    phi = Range(0, pi, auto_set = False, enter_set = True,
                 distr = ['sin_distr'])

    z = Float(0, auto_set = False, enter_set = True,
               distr = ['uniform'])

    f = Float(0.01, auto_set = False, enter_set = True,
               distr = ['uniform'])

    w = Float(ctrl_range = (0, 0.016, 20), auto_set = False, enter_set = True)

    C_code = '''
            double w = eps;
            double Le = L / 2. - z / cos( phi );
            double w_deb = exp( f * phi ) * qf * pow(Le,2.0) / E_mod / A;
            double P_deb_full = sqrt( 2. * w / 2. * E_mod * A * qf ) * exp( f * phi );
            double P_deb;
            
            // Heaviside
            if ( Le < 0 || P_deb_full > fu * A || w > w_deb ){
                P_deb = 0;
            }else{
                P_deb =P_deb_full;
            }
            
            double P_pull_x = ( Le * qf - Le * qf / ( Le - w_deb ) * ( w - w_deb ) ) * exp( f * phi );
            double P_pull;
            
            // Heaviside 
            if ( P_pull_x < 0 || w_deb > w ){
                P_pull = 0;
            }else{
                P_pull = P_pull_x;
            }
            
            // Computation of the q( ... ) function
            q = P_deb + P_pull;
        '''

    def __call__(self, w, fu, qf, L, A, E_mod, z, phi, f):
        '''Lexically optimized expresseion - each result is 
        calculated only once. 
        Further optimization possible by printing out the shape
        and doing inplace operation where possible.
        However, this does not seem to have a significant effect.
        '''
        t4 = sqrt(w * E_mod * A * qf)
        t5 = f * phi
        t6 = exp(t5)
        t7 = t4 * t6
        t11 = Heaviside(fu * A - 0.1000000000e1 * t7)
        t12 = exp(t5);
        t14 = 0.5000000000e0 * L
        t15 = cos(phi)
        t17 = z / t15
        t18 = t14 - t17
        t19 = pow(t18, 0.20e1)
        t24 = t12 * qf * t19 / E_mod / A
        t25 = t24 - w
        t26 = Heaviside(t25)
        t28 = Heaviside(t18)
        t32 = t18 * qf
        t38 = (t32 + t32 / (t14 - t17 - t24) * t25) * t6
        t39 = Heaviside(t38)
        t40 = Heaviside(-t25)
        res = 0.1000000000e1 * t7 * t11 * t26 * t28 + t38 * t39 * t40
        return res

def create_demo_object():

    #===========================================================================
    # Control variable
    #===========================================================================
    e_arr = np.linspace(0, 0.012, 80)

    #===========================================================================
    # Randomization
    #===========================================================================
    tvars = dict(#fu = 1200.0e6,
                 fu = RV('weibull_min', 1200.0e6, 200.),
                  qf = RV('uniform', 1500., 100.),
                  #qf = 1500.0,
                  L = 0.02, # 
                  # L = RV('uniform', 0.02, 0.02 / 2.),
                  A = 5.30929158457e-10,
                  #A = RV('norm', 5.30929158457e-10, .03 * 5.30929158457e-10),
                  E_mod = 70.0e9,
                  #E_mod = RV('uniform', 70.e9, 250.e9),
                  z = 0,
                  #z = RV('uniform', 0.0, 0.03),
                  phi = 0.0, # 
                  # phi = RV('cos_distr', 0.0, 1.0),
                  # phi = RV('uniform', 0.0, 1.0),
                  f = 0.01,
                  #f = RV('uniform', 0.0, 0.03),
                  )

    #===========================================================================
    # Integrator object
    #===========================================================================
    s = SPIRRID(q = ConstantFrictionFiniteFiber(),
                e_arr = e_arr,
                n_int = 10,
                tvars = tvars,
                )

    import pylab as p
    p.plot(e_arr, s.mu_q_arr)
    p.show()



if __name__ == '__main__':

    create_demo_object()

