using MatrixNetworks
using DelimitedFiles
A = MatrixNetworks.readSMAT("commutes-all.smat")
xy = readdlm("commutes-all.xy")
##
using SparseArrays
i = rand(1:size(A,1))
scatter(xy[:,1],xy[:,2],markersize=1, markerstrokewidth=0)
neighs,vals = findnz(A[:,i])
println(A[:,i].nzval)
scatter!([xy[i,1]], [xy[i,2]], markersize=9)
scatter!(xy[neighs,1],xy[neighs,2], markerstrokewidth=0, markersize=5, marker_z = vals)

##
##
using Plots
using GraphRecipes
using SparseArrays
src,dst = findnz(A)[1:2]
graphplot(src,dst,x = xy[:,1], y = xy[:,2],
  markersize=0, linewidth=0.5, linealpha=0.1)
