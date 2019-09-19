# Data Description
We crawled transcripts for the Rachel Maddow show and build a bipartite graph between show dates and people who appeared on that date. The crawl was performed on 9/18/2019 around 10:50PM. There is an edge between show i and person j if person j appeared on show i. 

The main website for transcripts can be found at: [http://www.msnbc.com/transcripts/rachel-maddow-show](http://www.msnbc.com/transcripts/rachel-maddow-show).


## Files
+ people.labels 
	* Names of people who appeared on the show. The person at index j has node label length(dates)+j (indexing starts from 0).  
+ show-dates.labels 
	* Dates of that the shows took place in chronological order. The date at index i is the date that corresponds to node i in the graph (indexing begins at 0).
+ maddow-edge-list.smat
	* An .smat representation of the bipartite graph. Nodes with IDs 0 - 2518 correspond to show dates in chronological order. Nodes with IDs 2519 - 4816 correspond to people. Given a person with node ID k, the name of that person is given by people[k-len(dates)]=people[k-2519]. For example, node label 4800 corresponds to 'ivor van heerden'. 
