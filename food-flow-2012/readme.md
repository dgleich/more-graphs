# Data Description 
The data we used is publically available from [https://www.census.gov/data/datasets/2012/econ/cfs/2012-pums-files.html](https://www.census.gov/data/datasets/2012/econ/cfs/2012-pums-files.html). This data has been anonymized. Se the above link for more details on how this is done. We extract flows for both the directed and undirected cases. In both instances, we formed unweighed graphs. We excluded flows that had some or all information concealed. 

#Files 
* locations.labels
    * file that contains the node id, node identifier in flows and the location. The identifier is simply the description for the identifier that was taken from the corresponding excel file at the above link. A single entry was manually added since it was missing from the excel file but it was present in the user guide.

* dir-food-flows.smat
    * the edge (i,j) represents that there was a flow of agricultural products from node i to node j.

* food-flows.smat
    * this is an undirected version of the above graph.

## Example
The edge (90,13) represents that there was a flow of agricultural products from 'Remainder of Ohio' to 'Remainder of California' (in the directed graph). In the undirected graph, this only represents that there was a flow between the two. 