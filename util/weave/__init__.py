#
# weave - C/C++ integration
#

from scipy.weave.info import __doc__
from scipy.weave.weave_version import weave_version as __version__

try:
    from scipy.weave.blitz_tools import blitz
except ImportError:
    pass # scipy (core) wasn't available

from inline_tools import inline
from scipy.weave import converters
import scipy.weave.ext_tools as ext_tools
from scipy.weave.ext_tools import ext_module, ext_function
try:
    from accelerate_tools import accelerate
except:
    pass

from numpy.testing import Tester
test = Tester().test
