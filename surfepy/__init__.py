from ._surfepy import *
import os

# add surfe package to path for C++ libs
os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + [pathlib.Path(surfepy.__file__).parent.resolve()]

