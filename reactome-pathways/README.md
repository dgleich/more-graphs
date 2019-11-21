Human Immune System Pathway Networks From Reactome
===========================

Reactome is a dataset to download known pathways among proteins or compounds in human system. Each pathway has multiple reactions involved and each reaction can have multiple inputs, outputs and catalysts. The output from one reaction can be input or catalyst for another reaction. Also there will be interactions between elements. This dataset will represent all the pathways from human immune system using a simple graph. In order to do that, each reaction will be represented as a dummy node and there will be four types of edges in this graph:

* A ---> B, directed edge, A is a reaction dummy node and B is one of the **outputs** of A
* C ---> A, directed edge, A is a reaction dummy node and C is one of the **inputs** of A
* D <---> A, undirected edge, A is a reaction dummy node and D is one of the **catalysts** of A
* B <---> C, undirected edge, B and C are elements of reactions and they also interacting with each other


Downloading the raw data
------------------------
Reactome is storing all the pathways in a Neo4j graph dataset. The full dataset can be downloaded at:

```
https://reactome.org/download/current/reactome.graphdb.tgz
```
For more information on the schema of this dataset, please refer to:

```
https://reactome.org/dev/graph-database
```

Building the graphs
------------------------
In order to build the graph, you need to download the dataset from Reactome as well as install Neo4j community version. After downloading, you will need to start a Neo4j console in the backend and replace the ```user```, ```token``` in ```reactome-pathways.py``` with yours. Then simply running the ```reactome-pathways.py``` will give you the following files:

* `reactome-pathway.smat` 

this file is the edge list of the built graph

* `reactome-pathway.smat`

this file has the metadata of each node, it is in the format of 

`id, reference dataset, element/reaction`

and sorted in the same order as the node indices. You can look up more information of each node by searching the `id` in its corresponding `reference dataset`. And reaction dummy node will have `reaction` in the third columns, otherwise, it will have `element`.