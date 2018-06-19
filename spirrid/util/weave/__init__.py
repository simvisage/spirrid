#
# weave - C/C++ integration
#

from numpy.testing import Tester
from weave import converters
from weave.ext_tools import ext_module, ext_function
from weave.version import version as __version__

from inline_tools import inline
import weave.ext_tools as ext_tools


try:
    from weave.blitz_tools import blitz
except ImportError:
    pass  # scipy (core) wasn't available

test = Tester().test
