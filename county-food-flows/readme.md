# Data Description 
The data that we used came from the supplementary data from Xiaowen Lin et al 2019 Environ. Res. Lett.14 084011. An online version of the paper as well as supplementary data can be found at [https://iopscience.iop.org/article/10.1088/1748-9326/ab29ae#supplementarydata](https://iopscience.iop.org/article/10.1088/1748-9326/ab29ae#supplementarydata). 

For the FIPS data that we used to generate the `counties.labels` file was obtained from [https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt](https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt) and was modified using three entries from [https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html](https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html). Namely the entries: 08014 Broomfield County, 12086 Miami-Dade County ,46102 Oglala Lakota County. 

All files are placed into a common directory and the python script is run from that directory. 

#### TODO specify how data was prepped for processing

# Files
* counties.labels
    * This file contains the county info that corresponds to node data. Note that there is a header file and node indices begin at 0.
* dir-county-flows.smat
    * edge (i,j) represents a food flow from county i to county j
* undir-county-flows.smat
    * same graph as above but undirected

## Examples
node 1555 corresponds to 'Barren County, Kentucky'. The edge (19,944) corresponds to a directed flow (or a flow in undirected case) from 'Delaware County, New York' to 'Norfolk County, Massachusetts'.