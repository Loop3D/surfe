import os
import pathlib
# add surfe package to path for C++ libs
os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + [pathlib.Path(__file__).parent.resolve()]

from ._surfepy import *
