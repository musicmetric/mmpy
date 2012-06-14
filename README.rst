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


Simple example
--------------

Here we fetch the chart of artists who bittorrent swarms have the highest acceleration rates and print the top 10

  $import mmpy
  $p2p = mmpy.Chart('downloads daily high flyers')
  $for rank, val, artist in p2p.artist[:10]:
  ...    print rank, ':', artist.name, ':', val
  ...:
  1 : Wiz Khalifa : 220.9106
  2 : Gotye : 200.7477
  3 : Train : 164.7793
  4 : Maroon 5 : 164.5974
  5 : David Guetta : 139.8408
  6 : The Wanted : 139.1948
  7 : Kimbra : 125.7001
  8 : Katy Perry : 125.0221
  9 : Carly Rae Jepsen : 113.4585
  10 : Morten Harket : 92.6741
  $


License
-------

This software is released and distributed under the ISC License, whose text is contained in LICENSE.txt.
