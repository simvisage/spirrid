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
# Created on Nov 8, 2011 by: rch

from enthought.traits.api import HasStrictTraits, Dict
from code_gen_numpy import CodeGenNumpy
from code_gen_compiled import \
    CodeGenCompiledTGrid, CodeGenCompiledPGrid, \
    CodeGenCompiledIrregular

#===============================================================================
# Factory classes to capture the dependency of C-code on the sampling type
#===============================================================================
class CodeGenNumpyFactory(HasStrictTraits):
    '''Just a single CodeGen for Numpy version.
    The code is not dependent on sampling type.
    '''
    def __call__(self, core):
        return CodeGenNumpy(core = core)

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
    def __call__(self, core):
        code_gen_type = self.mapping_table[ core.sampling_type ]
        return code_gen_type(core = core, ld = 'c')

class CodeGenCythonFactory(CodeGenCompiledFactory):
    '''Used codegen with cython-language .
    '''
    def __call__(self, core):
        code_gen_type = self.mapping_table[ core.sampling_type ]
        return code_gen_type(core = core, ld = 'cython')

