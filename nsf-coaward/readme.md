# Data Description 
The data we used is publicly available from the [National Science Foundation](https://www.nsf.gov/). Using NSF award data, we generate a "coaward" network. There is an edge from researcher i to researcher j if both researchers won an NSF award together. In order to avoid ambiguity with names, we use the internal NSF_ID for researchers when available. Note that only awards in which the NSF_ID for researchers is complete were used.<br><br>

Awards up to 2022 were manually downloaded in accordance with NSFs [robots.txt](https://www.nsf.gov/robots.txt) file. Files were unzipped by year and placed in the **data/** subdirectory but not included in the repository.

# Files
`main.py` 
  - script for producing edges and researcher information from raw data.
  
`nsf-coaward.smat`
- An .smat representation of the nsf-coaward network. Nodes represent researchers while edge represent the total award amount for awards containing both researchers. This is an undirected graph with self loops (representing solo-awards). 


`researchers.txt` 
- This file contains information about researchers as a tab-delimited file. It contains node_id,  researcher_name, and NSF_ID. 

### Example
The node with id "143574" refers to "david_gleich". In the .SMAT file, the self-loop at "143574" has weight "1658487", which is the total amount awarded to "david_gleich" in solo-awards by the NSF.

