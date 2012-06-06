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

from etsproxy.traits.api import HasTraits, Trait, Callable, Dict, \
    Str, Property, DelegatesTo, on_trait_change, \
    cached_property
from spirrid.sampling import FunctionRandomization, TGrid, \
    PGrid, MonteCarlo, LatinHypercubeSampling, make_ogrid
from spirrid.code_gen_factory import CodeGenNumpyFactory, \
    CodeGenCFactory, CodeGenCythonFactory
from spirrid.rv import RV

class SPIRRID(FunctionRandomization):
    '''Algorithmic class for multivariate random problem.
    '''
    sampling_type = Trait('TGrid',
                          {'TGrid' : TGrid,
                           'PGrid' : PGrid,
                           'MCS' : MonteCarlo,
                           'LHS': LatinHypercubeSampling },
                          sampling = True)
    sampling = Property(depends_on = 'sampling')
    @cached_property
    def _get_sampling(self):
        return self.sampling_type_(randomization = self)    

    codegen_type = Trait('numpy',
                         {'numpy' : CodeGenNumpyFactory(),
                          'weave' : CodeGenCFactory(),
                          'cython' : CodeGenCythonFactory()},
                         codegen = True)
    codegen = Property(depends_on = 'sampling, codegen')
    @cached_property
    def _get_codegen(self):
        return self.codegen_type_(spirrid = self)

    mu_q_arr = Property(depends_on = 'sampling, codegen')
    @cached_property
    def _get_mu_q_arr(self):
        '''getter for mean value array property .
        '''
        e_orth = make_ogrid(self.evar_lst)
        mu_q_method = self.codegen.get_code() 
        mu_q_arr, var_q_arr = mu_q_method(*e_orth)
        return mu_q_arr

if __name__ == '__main__':
    s = SPIRRID(q = lambda eps, theta: theta * eps,
                evars = {'eps' : [0.1, 0.2, 0.3] },
                tvars = {'theta' : RV('norm', 1.0, 1.0)})
    print 'mean values', s.mu_q_arr
