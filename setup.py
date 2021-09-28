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
from os.path import join

class CustomInstallLibCommand(install_lib):
    def run(self):
        install_lib.run(self)
        if os.path.isdir(self.build_dir):
            files = ['libmath_lib.so','libsurfe_lib.so']
            if sys.platform == 'win32':
                files = ['math_lib.dll','surfe_lib.dll']
            for f in files:
                shutil.copyfile(join(self.build_dir,Path('surfepy/{}'.format(f))),\
                join(self.install_dir,Path('../../{}'.format(f))))


    

setup(
    name="surfepy",
    version=0.51,
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
