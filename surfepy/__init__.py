import os
import pathlib
# add surfe package to path for C++ libs
if 'LD_LIBRARY_PATH' in os.environ:
    os.environ['LD_LIBRARY_PATH']=os.environ['LD_LIBRARY_PATH']+':{}'.format(pathlib.Path(__file__).parent.resolve())
else:
    os.environ['LD_LIBRARY_PATH'] = pathlib.Path(__file__).parent.resolve()

from ._surfepy import *
