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

from .code_gen_compiled import CodeGenCompiledTGrid, CodeGenCompiledPGrid, \
    CodeGenCompiledIrregular
from .code_gen_numpy import CodeGenNumpy
from etsproxy.traits.api import HasStrictTraits, Dict

#===============================================================================
# Factory classes to capture the dependency of C-code on the sampling type
#===============================================================================
class CodeGenNumpyFactory(HasStrictTraits):
    '''Just a single CodeGen for Numpy version.
    The code is not dependent on sampling type.
    '''
    def __call__(self, spirrid):
        return CodeGenNumpy(spirrid = spirrid)

class CodeGenCompiledFactory(HasStrictTraits):
    '''Depending on the sampling type return .
    '''
    mapping_table = Dict(value = {'TGrid' : CodeGenCompiledTGrid,
                                  'PGrid' : CodeGenCompiledPGrid,
                                  'MCS' : CodeGenCompiledIrregular,
                                  'LHS' : CodeGenCompiledIrregular
                                  })

class CodeGenCFactory(CodeGenCompiledFactory):
    '''Used codegen with c-language .
    '''
    def __call__(self, spirrid):
        code_gen_type = self.mapping_table[ spirrid.sampling_type ]
        return code_gen_type(spirrid = spirrid, ld = 'weave')

class CodeGenCythonFactory(CodeGenCompiledFactory):
    '''Used codegen with cython-language .
    '''
    def __call__(self, spirrid):
        code_gen_type = self.mapping_table[ spirrid.sampling_type ]
        return code_gen_type(spirrid = spirrid, ld = 'cython')

