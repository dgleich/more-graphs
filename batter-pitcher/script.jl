include("code_needed.jl")
myedge_list,names_data = run_script()
# reformat data to smat
writeToSMAT(myedge_list,"batter_pitcher_edges.smat")
writedlm("batter_pitcher_names.labels",names_data)