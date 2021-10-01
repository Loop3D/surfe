import sys
from setuptools.command.install import install
# from setuptools.command import bdist

from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install_lib import install_lib

try:
    from skbuild import setup
except ImportError:
    print("scikit-build is required to build from source!", file=sys.stderr)
    print("Install it running: python -m pip install scikit-build")
    sys.exit(1)

# class CustomInstallLibCommand(bdist):
#     def run(self):
#         bdist_wheel.run(self)
#         if os.path.isdir(self.build_dir):
#             shutil.copyfile(self.build_dir+'/surfepy/libmath_lib.so','/usr/lib/libmath_lib.so')
#             shutil.copyfile(self.build_dir+'/surfepy/libsurfe_lib.so','/usr/lib//libsurfe_lib.so')

#             # shutil.copyfile(join(self.build_dir,Path('/surfepy/libmath_lib.{}'.format(ext)),self.install_dir+'../../libmath_lib.{}'.format(ext))
            # shutil.copyfile(self.build_dir+'/surfepy/libsurfe_lib.{}'.format(ext),self.install_dir+'../../libsurfe_lib.{}'.format(ext))     

setup(
    name="surfepy",
    version=0.51,
    author="Michael Hillier",
    description="python bindings for surfe - geological interpolator using rbf",
    long_description="",
    license="MIT",
    cmake_args=['-DEIGEN3_INCLUDE_DIR=eigen-git-mirror',
               '-DCMAKE_INSTALL_RPATH="$ORIGIN/../lib:$ORIGIN/../..'],
    packages=['surfepy'],
    cmake_install_dir="surfepy",
    # extra_objects=['libmath_lib','libsurfe_lib']
    )
