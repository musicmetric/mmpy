mmpy
====

This is the officially supported python wrapper for Musicmetric http REST api. This API provides direct access to much of the data we use to drive our products.  This data is available for a wide array of music artists; in general, the more popular an artist is, the more likely there is going to be data.     


We provide the following data and services:

* Time series data of fan activity on a set of social networks,
* Sentiment analysis service for music related text
* Fan demographics
* a variety of lists and charts


The full API documentation can be found at http://developer.musicmetric.com


What to do with your API key
----------------------------

In order to use this wrapper with the Musicmetric API, you need to place your API key in one of two places:

* In an environment variable 'SEMETRIC_KEY'
* In a config file, expected to be a ~/.semetric/config that should contain the following lines::

  > [semetric]
  > api.key = YOUR_KEY
  


both of these are checked at run time in the order listed. The first key found will be used (ie. if there's a key in env, this will be used and the config file will be ignored).


This software is released and distributed under the ISC License, whose text is contained in LICENSE.txt.
