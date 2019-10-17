## Data Description

The IMDb graph is similar to the Hollywood graph or the [co-stardom network](https://en.wikipedia.org/wiki/Co-stardom_network), 
which is the collaboration graph of movie directors or writers. In this graph, two directors or writers are joined by 
an edge if they have worked in a movie or a show together.

## Data Source
IMDb Datasets: https://datasets.imdbws.com/  
Dataset Description: https://www.imdb.com/interfaces/

## Graph Structure
G = (V, E, W) \[weighted, undirected\]  
V: a set of directors or writers with unique IMDb Id  
E: whether co-worked in a movie or a show  
W: the number of collaborative works

## Files
+ IMDb_{directors / writers}.labels
	* the actual name of directors or writers for each row
+ IMDb_{directors / writers}.smat
	* An .smat representation of the co-working graph.  
	
## Notice
+ We only keep the node which has at least one edge. This can be adjusted through the parameter $thrd, which indicates the
minimal linkage between nodes.

+ There are some duplicated node Id in the original data. For consistency, We use a dict ('alias') to replace all of them.
It also contains some Id without corresponding records. In this case, we leave the label as it is.

+ The use of IMDb data is subject to IMDb's terms and conditions. Personal and Limited non-commercial use are allowed.  
For details, please refer to the [Non-Commercial Licensing](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3aefe545-f8d3-4562-976a-e5eb47d1bb18&pf_rd_r=TW7K7399H579FZ4EZJ8F&pf_rd_s=center-1&pf_rd_t=60601&pf_rd_i=interfaces&ref_=fea_mn_lk1) 
and [copyright/license](https://www.imdb.com/conditions?ref_=helpms_ih_gi_usedata) and verify compliance.
