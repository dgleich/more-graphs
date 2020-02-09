##
using MatrixNetworks
using DelimitedFiles
using CSV
A = MatrixNetworks.readSMAT("cropsim-2010-harvestarea.smat")
xy = readdlm("cropsim-2010-harvestarea.xy")
##
df = CSV.read("cropsim-2010-harvestarea-metadata.csv"; header=false)
##
using Plots
## Show the magnitude of the harvest at each area.
scatter(xy[:,1],xy[:,2],markersize=1, markerstrokewidth=0, marker_z = df.Column4)
## Show the degrees
scatter(xy[:,1],xy[:,2],markersize=1, markerstrokewidth=0, marker_z = sum(A,dims=2))
##
using SparseArrays
i = rand(1:size(A,1))
scatter(xy[:,1],xy[:,2],markersize=1, markerstrokewidth=0)
neighs,vals = findnz(A[:,i])
println(A[:,i].nzval)
scatter!([xy[i,1]], [xy[i,2]], markersize=9)
scatter!(xy[neighs,1],xy[neighs,2], markerstrokewidth=0, markersize=5, marker_z = vals)
