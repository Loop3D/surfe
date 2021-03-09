import os, sys
# add the installation folder to the path so that the c++ libs can be used
sys.path.append(os.path.dirname(__file__))
from ._surfepy import *