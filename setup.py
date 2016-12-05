import os
import sys
sys.path.insert(0, os.path.abspath("."))
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

extensions = [
	Extension("src.clustering_m.clustering", ["./src/clustering_m/clustering.pyx"],
		include_dirs = [numpy.get_include()]),	
		]

setup(
	# cmdclass = { 'build_ext': build_ext},
	ext_modules = cythonize(extensions),
)