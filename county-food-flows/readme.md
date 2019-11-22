# Data Description 
The data that we used came from the supplementary data from Xiaowen Lin et al 2019 Environ. Res. Lett.14 084011. An online version of the paper as well as supplementary data can be found at [https://iopscience.iop.org/article/10.1088/1748-9326/ab29ae#supplementarydata](https://iopscience.iop.org/article/10.1088/1748-9326/ab29ae#supplementarydata). 

For the FIPS data that we used to generate the `counties.labels` file was obtained from  [https://github.com/dgleich/more-graphs/tree/master/misc-county-fips-data](https://github.com/dgleich/more-graphs/tree/master/misc-county-fips-data).


# Files
* dir-county-flows.smat
    * edge (i,j) represents a food flow from county i to county j
* undir-county-flows.smat
    * same graph as above but undirected
* counties.labels
    * This file contains the county info that corresponds to node data. The first line corresponds to node 0.
* counties.xy
    * represents xy coords (latitude and longitude) for each county. Note that the first entry corresponds to node 0
* full-county-info.xy
    * this is just a concatenation above the above two files for convenience and clarity. Note that the first line corresponds to node 0.


## Examples
node 1555 corresponds to 'Phelps, MO'. The edge (31,164) corresponds to a directed flow (or a flow in undirected case) from 'Greene, AL' to 'Randolph, AR'.