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
# Created on Sep 29, 2011 by: rch

import numpy
from time import sleep
import enthought.mayavi.mlab as m
from core import SPIRRID, RV, make_ogrid
from quaducom.resp_func.cb_clamped_fiber import CBClampedFiberSP
import numpy as np
import os.path
import string
import tempfile

if __name__ == '__main__':

    q = CBClampedFiberSP()

    s = SPIRRID(q = q,
                sampling_type = 'LHS',
                evars = dict(w = np.linspace(0.0, 0.4, 50),
                             x = np.linspace(-20.1, 20.5, 100),
                             Lr = np.linspace(0.1, 20.0, 50)
                             ),
                tvars = dict(tau = RV('uniform', 0.7, 1.0),
                             l = RV('uniform', 5.0, 10.0),
                             D_f = 26e-3,
                             E_f = 72e3,
                             theta = 0.0,
                             xi = RV('weibull_min', scale = 0.017, shape = 8, n_int = 10),
                             phi = 1.0,
                             Ll = 50.0,
#                              Lr = 1.0
                             ),
                n_int = 5)

    e_arr = make_ogrid(s.evar_list)
    n_e_arr = [ e / np.max(np.fabs(e)) for e in e_arr ]

    max_mu_q = np.max(np.fabs(s.mu_q_arr))
    n_mu_q_arr = s.mu_q_arr / max_mu_q
    n_std_q_arr = np.sqrt(s.var_q_arr) / max_mu_q

    #===========================================================================
    # Prepare plotting 
    #===========================================================================
    tdir = tempfile.mkdtemp()
    n_img = n_mu_q_arr.shape[0]
    fnames = [os.path.join(tdir, 'x%02d.jpg' % i) for i in range(n_img) ]

    f = m.figure(1, size = (1000, 500), fgcolor = (0, 0, 0),
                 bgcolor = (1., 1., 1.))

    s = m.surf(n_e_arr[1], n_e_arr[2], n_mu_q_arr[0, :, :])
    ms = s.mlab_source

    m.axes(s, color = (.7, .7, .7),
           extent = (-1, 1, 0, 1, 0, 1),
           ranges = (-0.21, 0.21, 0.1, 20, 0, max_mu_q),
           xlabel = 'x[mm]', ylabel = 'Lr[mm]',
           zlabel = 'f[N]',)
    m.view(-60.0, 70.0, focalpoint = [0., 0.45, 0.45])

    m.savefig(fnames[0])

    for i, fname in enumerate(fnames[1:]):
        ms.scalars = n_mu_q_arr[i, :, :]
        m.savefig(fname)

    images = string.join(fnames, ' ')
    destination = os.path.join('fig', 'fiber_cb_8p_anim.gif')

    import platform
    if platform.system() == 'Linux':
        os.system('convert ' + images + ' ' + destination)
    else:
        raise NotImplementedError, 'film production available only on linux'

    m.show()
