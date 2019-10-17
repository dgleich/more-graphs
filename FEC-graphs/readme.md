# Data Description 
The data used here is available from [https://www.fec.gov/data/browse-data/?tab=bulk-data](https://www.fec.gov/data/browse-data/?tab=bulk-data).
In particular we used "Any transaction from one committee to another" (these are the 'oth' files) and "Contributions from committees to candidates & independent expenditures" (these are the 'pas' files). Note that the 'pas' files are actually a subset of the interactions of the 'oth' files. Also note that to retrieve the name of the committees see the "Committee master" data in the above website. More details about the data can also be found there as well.

The data is downloaded and unzipped into a common directory from which the `main.py` file in run in that directory. Note that this data does not include "soft money" transactions. Data for committee names are retrieved from [https://www.fec.gov/data/committees/](https://www.fec.gov/data/committees/)

# Files
* oth**.labels files
    * CommitteeID for the node labels. CommitteeIDs are sorted and the index in this sorted list is used as the node id (we begin indexing at 0). The same node label is used for both the directed and undirected graph. This is for the 2 year period ending in the listed number, i.e. oth84.labels is the labels for transaction period 1982-1984.

* oth**.smat files
    * These are the files for the undirected graph. So committee i has an edge with committee j if there was an flow of money between these two communities at any time over the 2 year period. Note that self-loops (if any) are included. 

* oth**-directed.smat files
    * These are directed and weighted graphs representing if there was a nonzero net flow of money between two committees over the two year period. So if committee i sent committee j 1000 in net flow we have the edge i j 1000.
* pas2** files
    * These are similar to the above files except that they are a subset of the original transaction data and contain transaction data about contributions from committees to candidates and independent expenditures.
* committee-names.labels
    * File of committee IDs and names for all committees.