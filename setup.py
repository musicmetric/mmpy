#!/usr/bin/env python
import sys, os.path
import ConfigParser
from distutils.core import setup

setup(name='mmpy',
      version='0.1dev',
      description='Musicmetric API Wrapper',
      long_description="""This is the officially supported python wrapper for Musicmetric REST api.  This API provides direct access to much of the data we use to drive our products.  This data is available for a wide array of music artists; in general, the more popular an artist is, the more likely there is going to be data.

      We provide the following data and services:

      - Time series data of fan activity on a set of social networks,
      - Sentiment analysis service for music related text
      - Fan demographics
      - a variety of lists and charts""",
      author='Ben Fields',
      author_email='ben@musicmetric.com',
      url='https://github.com/musicmetric/mmpy',
      packages=['mmpy'],
      package_dir={'mmpy':'src'},
      provides=['mmpy'],
      license='ISC License',
      requires=['simplejson']
      )
