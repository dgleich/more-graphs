include("code_needed.jl")
edge_list,name_ids,names_data = run_script()
# reformat data to smat
writeToSMAT(edge_list,"batter_pitcher_edges.smat")
writedlm("batter_pitcher_names.labels",names_data)