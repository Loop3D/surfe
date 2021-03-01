import sys
from setuptools.command.install import install
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

class CustomInstallLibCommand(install_lib):
    def run(self):
        install_lib.run(self)
        if os.path.isdir(self.build_dir):
            shutil.copyfile(self.build_dir+'/surfepy/libmath_lib.so',self.install_dir+'../../libmath_lib.so')
            shutil.copyfile(self.build_dir+'/surfepy/libsurfe_lib.so',self.install_dir+'../../libsurfe_lib.so')

    

setup(
    name="surfepy",
    version=0.2,
    author="Michael Hillier",
    cmdclass={
        'install_lib': CustomInstallLibCommand
    },
    description="python bindings for surfe - geological interpolator using rbf",
    long_description="",
    license="MIT",
    cmake_args=['-DEIGEN3_INCLUDE_DIR=eigen-git-mirror'],
    packages=['surfepy'],
    cmake_install_dir="surfepy"
    )
