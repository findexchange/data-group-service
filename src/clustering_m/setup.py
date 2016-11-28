from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
  name = 'clustering app',
  ext_modules = cythonize("./clustering.pyx"),
  include_dirs=[numpy.get_include()]
)