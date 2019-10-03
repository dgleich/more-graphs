## Data Description
This is a word occurence graph constructed from a bunch of chinese news articles with its topic to be politics. Nodes are words and two words will be connected if they show up in the same sentence. The edge weight is calculated by pointwise mutual information. 

## Filtering Pocedure
A word is counted only when it satisfies all the criteria

+ it shows up at least twice
+ it has at least two characters
+ it cannot be numerical digits or english characters or punctuations

Also, edges with weight below or equal 0.01 are filtered out. (there are 10926 such edges) The final graph has 23608 nodes and 5995666 edges.

The dataset is downloaded from 

[https://www.kaggle.com/louislung/categorised-news-dataset-from-fudan-university]()

And we only choose the first 500 articles based on ascending sorted filenames inside train/C34-Economy/
We use the following package to segment each article into words.

[https://github.com/fxsjy/jieba]()

## Files
+ words_coocurrence.labels
	* the actual words for each row
+ maddow-edge-list.smat
	* An .smat representation of the coocurrance graph.
