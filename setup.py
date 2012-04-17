#!/usr/bin/env python
import sys, os.path
import ConfigParser

try:
    from setuptools import setup
except:
    from distutils.core import setup


setup(name='mmpy',
      version='0.1.4dev',
      description='Musicmetric API Wrapper',
      long_description=open('README.rst').read(),
      author='Ben Fields',
      author_email='ben@musicmetric.com',
      url='https://github.com/musicmetric/mmpy',
      packages=['mmpy'],
      package_dir={'mmpy':'src'},
      provides=['mmpy'],
      license='ISCL',
      install_requires=['simplejson'],
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: ISC License (ISCL)',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent']
      )
