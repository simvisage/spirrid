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

from code_gen import CodeGen
import numpy as np

#===============================================================================
# Generator of the numpy code
#===============================================================================
class CodeGenNumpy(CodeGen):
    '''
        Numpy code is identical for all types of sampling, 
        no special treatment needed. 
    '''
    def get_code(self):
        '''
            Return the code for the given sampling of the random domain.
        '''
        s = self.spirrid
        n = len(s.evar_lst)
        targs = dict(zip(s.tvar_names, s.sampling.theta))

        if self.implicit_var_eval:

            def mu_q_method(*e):
                '''Template for the evaluation of the mean response.
                '''
                eargs = dict(zip(s.evar_names, e))
                args = dict(eargs, **targs)

                Q_dG = s.q(**args)
                Q2_dG = Q_dG ** 2

                Q_dG *= s.sampling.dG  # in-place multiplication
                Q2_dG *= s.sampling.dG

                # sum all squared values to get the variance
                mu_q = np.sum(Q_dG)
                var_q = np.sum(Q2_dG) - mu_q ** 2

                return mu_q, var_q
        else:

            def mu_q_method(*e):
                '''Template for the evaluation of the mean response.
                '''
                eargs = dict(zip(s.evar_names, e))
                args = dict(eargs, **targs)

                Q_dG = s.q(**args)

                Q_dG *= s.sampling.dG  # in-place multiplication

                # sum all squared values to get the variance
                mu_q = np.sum(Q_dG)

                return mu_q, None
        # otypes list of the length n = number of output parameters of mu_q_method
        # mu_q, var_q => 2
        otypes = [ float for i in range(2)]
        return np.vectorize(mu_q_method, otypes=otypes)

    def __str__(self):
        return 'numpy\nvar_eval: %s\n' % `self.implicit_var_eval`

