Facebook County-level Connections
===========================

The New York Times published a great article about
the county-level connections that exist in Facebook
based on an article in the Journal of Economic
Perspectives. Please cite the following sources
for this data.

```
@article{Bailey2018,
  doi = {10.1257/jep.32.3.259},
  url = {https://doi.org/10.1257/jep.32.3.259},
  year = {2018},
  month = aug,
  publisher = {American Economic Association},
  volume = {32},
  number = {3},
  pages = {259--280},
  author = {Michael Bailey and Rachel Cao and Theresa Kuchler and Johannes Stroebel and Arlene Wong},
  title = {Social Connectedness: Measurement,  Determinants,  and Effects},
  journal = {Journal of Economic Perspectives}
}
@article{Badger2018,
  title = {How Connected Is Your Community to Everywhere Else in America?},
  author = {Emily Badger and Quoctrung Bui},
  year = {2018},
  month = sep,
  journal = {The New York Times},
  volume = {2018},
  howpublished = {\url{https://www.nytimes.com/interactive/2018/09/19/upshot/facebook-county-friendships.html}}
}
```

Downloading the raw data
------------------------
```
wget https://static01.nyt.com/newsgraphics/2018/08/13/fb-friendships/c15239849eab44f7bc5b2cd9d17c67821dfb071f/county2county.binary

wget https://static01.nyt.com/newsgraphics/2018/08/13/fb-friendships/c15239849eab44f7bc5b2cd9d17c67821dfb071f/county-info.csv

wget
https://static01.nyt.com/newsgraphics/2018/08/13/fb-friendships/c15239849eab44f7bc5b2cd9d17c67821dfb071f/top.csv

wget
https://static01.nyt.com/newsgraphics/2018/08/13/fb-friendships/c15239849eab44f7bc5b2cd9d17c67821dfb071f/final-map.json
```

This gets the three files that are most important.

Our script to turn these into a graph and associated set of
metadata use an additional table from Wikipedia

>  https://en.wikipedia.org/wiki/User:Michael_J/County_table

and is reproduced here as `wikipedia-county-info.jl`.

Building the graphs
-------------------

The script `parse_county_network.jl` builds the graphs

* `facebook-county-friendship.smat`
* `facebook-county-friendship-top10.smat`
* `facebook-county-friendship-nonsym.smat`

There are three graphs here because the data is mostly
symmetric, but there are a few non-symmetric entries,
which are stored as corrections in the `-nonsym.smat` file
(I think it is safe to ignore them.)

The `-top10.smat` just lists the top10 closest connections
for each county.

Each entry is between 1 and 7 with 7 indicating super-strong
connection (see the NYTimes page) and 1 indicating the weakest
connect. Note that the original NYTimes data has entries between 1 and 8
where every entry is at least 1. We filtered these to 0-7 and skipped
all the ones.

There are disconnected counties in Virginia in our data.

```
"Covington, VA"    
"Emporia, VA"      
"Fairfax City, VA"      
"Lexington, VA"    
"Manassas Park, VA"
"Martinsville, VA"
```

The metadata
------------
The script `county-info-wiki.jl` will output the files
* `facebook-county-friendship.labels` which gives each county name and state
* `facebook-county-friendship.xy` which gives the lat-long of the county center
* `facebook-county-friendship-metadata.csv` which gives the population and area of each county too.
