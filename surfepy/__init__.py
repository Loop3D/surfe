import os
import pathlib
# add surfe package to path for C++ libs

try:
    from ._surfepy import *
except ImportError:
    if 'LD_LIBRARY_PATH' in os.environ:
        if 'surfepy' not in os.environ['LD_LIBRARY_PATH']:
            os.environ['LD_LIBRARY_PATH']=os.environ['LD_LIBRARY_PATH']+':{}'.format(pathlib.Path(__file__).parent.resolve())
    else:
        os.environ['LD_LIBRARY_PATH'] = pathlib.Path(__file__).parent.resolve()

try:
    from ._surfepy import *
except ImportError:
    raise ImportError('Could not import surfepy. Please make sure that the surfepy package is installed.')