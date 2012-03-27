#!/usr/bin/env python
import sys, os.path
import ConfigParser
from distutils.core import setup

setup(name='mmpy',
      version='0.1',
      description='Musicmetric API Wrapper',
      long_description=open('README.md').read(),
      author='Ben Fields',
      author_email='ben@musicmetric.com',
      url='https://github.com/musicmetric/mmpy',
      packages=['mmpy'],
      package_dir={'mmpy':'src'},
      provides=['mmpy'],
      license='LICENSE.txt',
      requires=['simplejson']
      )
