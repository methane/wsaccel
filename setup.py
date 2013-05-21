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
    if os.path.exists(pyx):
        if not os.path.exists(src) \
           or os.stat(src).st_mtime < os.stat(pyx).st_mtime:
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
        cythonize('wsaccel/utf8validator.pyx')
        cythonize('wsaccel/xormask.pyx')
        sdist.__init__(self, *args, **kwargs)

ext_modules = [
    Extension('wsaccel.utf8validator', ['wsaccel/utf8validator.c']),
    Extension('wsaccel.xormask', ['wsaccel/xormask.c']),
    ]

with open('README.rst') as f:
    long_description = f.read()

setup(name="wsaccel",
      version='0.6.2',
      description="Accelerator for ws4py and AutobahnPython",
      maintainer="INADA Naoki",
      maintainer_email="songofacandy@gmail.com",
      url="https://github.com/methane/wsaccel",
      packages=["wsaccel"],
      cmdclass={'build_ext': BuildExt, 'sdist': Sdist},
      ext_modules=ext_modules,
      platforms=["any"],
      license='Apache',
      long_description=long_description,
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
