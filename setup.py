# -*- coding: utf-8 -*-
import os
import sys
import subprocess
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from distutils.command.build_ext import build_ext
from distutils.command.sdist import sdist


class NoCython(Exception):
    pass

def cythonize(src):
    sys.stderr.write("cythonize: %r\n" % (src,))
    subprocess.check_call("cython '%s'" % (src,), shell=True)

def ensure_source(src):
    pyx = os.path.splitext(src)[0] + '.pyx'
    if not os.path.exists(src):
        if not have_cython:
            raise NoCython
        cythonize(pyx)
    elif (os.path.exists(pyx) and
          os.stat(src).st_mtime < os.stat(pyx).st_mtime and
          have_cython):
        cythonize(pyx)
    return src


class BuildExt(build_ext):
    def build_extension(self, ext):
        try:
            ext.sources = list(map(ensure_source, ext.sources))
        except NoCython:
            print("Cython is required for building extension from checkout.")
            print("Install Cython >= 0.16 or install ws4py from PyPI.")
            raise
        return build_ext.build_extension(self, ext)


class Sdist(sdist):
    def __init__(self, *args, **kwargs):
        cythonize('cutf8validator/utf8validator.pyx')
        sdist.__init__(self, *args, **kwargs)

ext_modules = [
    Extension('cutf8validator.utf8validator',
              ['cutf8validator/utf8validator.c']),
    ]


setup(name = "cutf8validator",
      version = '0.1',
      description = "Faster Utf8Validator for WS4PY and Autobahn",
      maintainer = "INADA Naoki",
      maintainer_email = "songofacandy@gmail.com",
      url = "https://github.com/methane/cutf8validator",
      packages = ["cutf8validator"],
      cmdclass={'build_ext': BuildExt, 'sdist': Sdist},
      ext_modules=ext_modules,
      platforms = ["any"],
      license = 'Apache',
      long_description = "UTF-8 Validator implemented in Cython.\n"
            "Faster replacement for utf8validator in ws4py and Autobahn.",
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          ],
     )
