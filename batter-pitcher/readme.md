### Quick notes about this data:
## To regenerate:
- Data was retrieved from: https://github.com/nassarhuda/data_crawls/tree/master/batter_pitcher
- All relevant information about the data and crawler should be found in that repo.
- If you download the above repo, you will have the data needed.
- Place `code_needed.jl` and `script.jl` in the same folder and run `include("script.jl")` from a julia session.
- This should generate the `.smat` and `.labels` files.

## Files
- `batter_pitcher_names.labels`: Labels are arranged in order, i.e. node `i` in the network corresponds to row `i` in the labels file. Each labels line has two pieces of information, the first is the player id from the original website https://www.retrosheet.org/retroID.htm, and the second piece of information is the player's name.
- `batter_pitcher_edges.smat`: smat file of batter pitcher games, where players are indexed from zero. 
Top of the file looks like:
```
19952   19952   815493 
1	12	1
1	26	1
1	47	1
1	51	1
1	174	1
1	326	1
1	317	1
1	362	1
1	402	1

```
The top line indicates that there are 19952 nodes, and 815493 edges. The rest of the lines are `<playerid_1> <playerid_2> 1`, where is the first player `<playerid_1>` was the batter in that match, and the second player `<playerid_2>` is the pitcher. This is an unweighted graph, and thus the weights are understood to be 1.