Data
----

This data includes census-tract level commute data in the US as a simple flow.
Each node is a census tract district with a few thousand people.
Each edge is a commuter relationship. The data are described in the first
paper below.

Files
-----

- `commutes-all.smat` has the flow/measure of error ratio for all 4 million commutes in the database.
- `commutes-all}.xy` has the long-lat for all nodes. Each line has the long-lat for the node with corresponding id.
- `commutes-all.labels` has the census tract GEOID for each node. This is a concatenation of the 2-digit state FIPS code, 3-digit county FIPS code, and 6-digit tract code. So each is 11 digits. The first 5 digits are the county FIPS codes.

If you want population, you can get it from the CenPop2010 dataset mentioned below -- see `process-data.jl` for how to map data to that dataset.

Notes
-----

The graph is not connected. The weights are what were used for community analysis in the citation below.

Citation.
---------
    @article{Nelson-2016-us-commutes,
        author = {Dash, Nelson Garrett and Alasdair Rae},
        year = {2016},
        title = {An Economic Geography of the United States: From Commutes to Megaregions},
        journal = {PLoS ONE},
        volume = {11},
        issue = {11},
        pages = {e0166083},
        doi = {10.1371/journal.pone.0166083},
    }

Download data and unzip
-------------------

    wget https://figshare.shef.ac.uk/ndownloader/articles/4110156/versions/5 -O data.zip
    curl https://www2.census.gov/geo/docs/reference/cenpop2010/tract/CenPop2010_Mean_TR.txt -O
    unzip data.zip
    unzip us_ttw_v3_US_only_epsg5070v2.zip


If these instructions stop working. The you can find new links to the data at <https://doi.org/10.15131/shef.data.4110156>

Then the graph can be produced by `process-data.jl`

Usage
-----

To see an example of how to use it, see `test-data.jl`
