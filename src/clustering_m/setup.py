from distutils.core import setup
from distutils.core import Extension
from Cython.Distutils import build_ext
import numpy

extensions = [
	Extension("clustering", ["clustering.pyx"],
		include_dirs = [numpy.get_include()]),	
		]

setup(
	cmdclass = { 'build_ext': build_ext },
	ext_modules = extensions,
)