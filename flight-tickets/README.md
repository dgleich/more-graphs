US Flight Tickets Network
===========================

The Airline Origin and Destination Survey (DB1B) is a 10% sample of airline tickets from reporting carriers collected by the Office of Airline Information of the Bureau of Transportation Statistics.

Downloading the raw data
------------------------
There are three files you need to download in order to build this graph.

>  https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=247

>  https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=

Building the graphs
-------------------

The script `flight-tickets.jl` builds the following files

* `flight-tickets.smat` which gives the graph
* `us-airports.xy` which gives the lat-long of each airport
* `us-airports.labels` which gives airport names
* `us-airports-metadata.csv` which gives airport id, airport state name and airport city market id
