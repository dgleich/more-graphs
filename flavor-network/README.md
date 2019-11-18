A Flavor Network
================

The flavor network is a graph of relationships between food
ingredients based on what chemical compounds they share. There
is also an associated recipes list that gives information on
which combinations of foods use a subset of these
same ingredients. The
data originates with the following paper, which should
be cited if these data are used.

```
@article{Ahn2011,
  doi = {10.1038/srep00196},
  url = {https://doi.org/10.1038/srep00196},
  year = {2011},
  month = dec,
  publisher = {Springer Science and Business Media {LLC}},
  volume = {1},
  number = {1},
  author = {Yong-Yeol Ahn and Sebastian E. Ahnert and James P. Bagrow and Albert-L{\'{a}}szl{\'{o}} Barab{\'{a}}si},
  title = {Flavor network and the principles of food pairing},
  journal = {Scientific Reports}
}
```

Downloading the raw data
------------------------
The raw data is available in the supplementary CSV files
associated with `https://doi.org/10.1038/srep00196`.
Download the 2nd and 3rd supplementary files.
After unzipping them, the md5 values we had were.

MD5 (srep00196-s2.csv) = be229824f3d8e905f7d2a9e5ad49a6fd
MD5 (srep00196-s3.csv) = a08b59180cdfd398ca91bc3e46df9ddc


Building the graphs
-------------------

The script `parse_network.jl` builds the graphs
based on the files above. The outputs are

* `ingredient-net.smat` (and associated .labels)
* `recipes.smat` (and associated .labels)

The `ingredient-net.smat` graph is the
flavor network from the paper. This has 1507 compounds from
Fenaroli's handbook. Each edge indicates how many flavor
compounds each ingredient shares; the graph is undirected and
both edges (i,j) and (j,i) are present in the ``.smat` file.
This graph has a connected
component of 1496 ingredients. Each label is the
name of an ingredient.

The `recipes.smat` graph is a map from recipes to ingredients. This is
a bipartite graph. 
There is also metadata about what country each recipes comes from.
There are 56496 recipes. All of the ingredients can be mapped
except for `starch` and `condiment`, which are ignored. Note
that there are only 381 unique ingredients (or 379 without
starch and condiment). The labels are the cuisines associated
with the recipe.
