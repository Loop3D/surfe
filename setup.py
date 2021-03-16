import sys
from setuptools.command.install import install
# from setuptools.command.bdist_wheel import bdist_wheel

from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install_lib import install_lib

try:
    from skbuild import setup
except ImportError:
    print("scikit-build is required to build from source!", file=sys.stderr)
    print("Install it running: python -m pip install scikit-build")
    sys.exit(1)

import os
from pathlib import Path
import platform
import shutil
from os.path import join
import codecs
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# class CustomInstallLibCommand(bdist_wheel):
#     def run(self):
#         bdist_wheel.run(self)
#         print('yes****')
#         if os.path.isdir(self.build_dir):
#             shutil.copyfile(self.build_dir+'/surfepy/libmath_lib.so',self.install_dir+'/libmath_lib.so')
#             shutil.copyfile(self.build_dir+'/surfepy/libsurfe_lib.so',self.install_dir+'/libsurfe_lib.so')

#             # shutil.copyfile(join(self.build_dir,Path('/surfepy/libmath_lib.{}'.format(ext)),self.install_dir+'../../libmath_lib.{}'.format(ext))
#             # shutil.copyfile(self.build_dir+'/surfepy/libsurfe_lib.{}'.format(ext),self.install_dir+'../../libsurfe_lib.{}'.format(ext))   

setup(
    name="surfepy",
    version=get_version("surfepy/__init__.py"),
    author="Michael Hillier",
    description="python bindings for surfe - geological interpolator using rbf",
    long_description="",
    license="MIT",
    cmake_args=['-DEIGEN3_INCLUDE_DIR=eigen-git-mirror'],
    packages=['surfepy'],
    cmake_install_dir="surfepy",
    extra_objects=['libmath_lib','libsurfe_lib']
    )
