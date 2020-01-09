## Spectral clustering on artists
using DelimitedFiles
using SparseArrays
names = readlines("../2-unit-1-demos/artistsim.names")
data = readdlm("../2-unit-1-demos/artistsim.smat")
##
A = sparse(Int.(data[2:end,1]).+1,
           Int.(data[2:end,2]).+1,
           Int.(data[2:end,3]),
           Int(data[1,1]),Int(data[1,1]))
##
A = max.(A,A')
##
using PyCall
using Conda
pyimport_conda("igraph","python-igraph","conda-forge")
##
using PyCall
igraph = pyimport("igraph")

function igraph_layout(A::SparseMatrixCSC{T}, layoutname::AbstractString="drl") where T
    ei,ej,ew = findnz(A)
    edgelist = [(ei[i]-1,ej[i]-1) for i = 1:length(ei)]
    nverts = size(A)
    G = igraph.Graph(nverts, edges=edgelist, directed=false)
    xy = G.layout(layoutname)
    xy = [Float64(xy[i][j]) for i in 1:length(xy),  j in 1:length(xy[1])]
end

xy = igraph_layout(A, "drl")
##
writedlm("artistsim.xy", xy)
##
using GraphRecipes
using LinearAlgebra
using Plots
ei, ej = findnz(triu(A,1))
graphplot(ei, ej, x =xy[:,1], y=xy[:,2],
  markercolor=:black, markerstrokecolor=:white,
  size=(1200,1200),dpi=300,
  markersize=2, linecolor=1, linealpha=0.01, linewidth=0.5,
  markeralpha=0.2,
  axis_buffer=0.02, background=nothing)
#savefig("artistsim-plot.png")
