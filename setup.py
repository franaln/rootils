#! /usr/bin/env python
#
import os
from glob import glob

DISTNAME = 'rootils'
MAINTAINER = 'Francisco Alonso'
MAINTAINER_EMAIL = 'franaln@gmail.com'
URL = 'https://github.com/franaln/rootils'
LICENSE = ''
DOWNLOAD_URL = 'https://github.com/franaln/rootils'
VERSION = '0.1'
DESCRIPTION = "utils for ROOT"

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          #long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          include_package_data=True,
          packages=['rootils',],
          scripts=glob('scripts/*'),
          )
