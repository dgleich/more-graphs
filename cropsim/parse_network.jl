##
using CSV
datadir = "/Users/dgleich/Downloads/spamdir/"
using SparseArrays
function writeSMAT(filename::AbstractString, A::SparseMatrixCSC{T,Int}; values::Bool=true) where T
    open(filename, "w") do outfile
        write(outfile, join((size(A,1), size(A,2), nnz(A)), " "), "\n")

        rows = rowvals(A)
        vals = nonzeros(A)
        m, n = size(A)
        for j = 1:n
           for nzi in nzrange(A, j)
              row = rows[nzi]
              val = vals[nzi]
              if values
                write(outfile, join((row-1, j-1, val), " "), "\n")
              else
                write(outfile, join((row-1, j-1, 1), " "), "\n")
              end
           end
        end
    end
end

## 2000 - harvested area
data2000h = CSV.read("$datadir/spam_h.csv")
data = data2000h
data = data[data.stat_code .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[10:29]
X = Matrix(data[:,10:29])
##
#=
using LinearAlgebra
f = norm.(eachrow(X)) .> 0.1)
data = data[f,:]
X = X[f,:]
=#
##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
##
# G = nngraph(idxs[1:45,:],dsts[1:45,:])
G = nngraph(idxs,dsts)

##
using Pkg
if haskey(Pkg.installed(), "MatrixNetworks")
  using MatrixNetworks
  @show is_connected(G)
end

##
using DelimitedFiles
writeSMAT("cropsim-2000-harvestarea.smat",G)
writedlm("cropsim-2000-harvestarea.xy", zip(data.x,data.y))
##
writedlm("cropsim-2000-harvestarea-metadata.csv",
    zip(data.alloc_key, data.hc_seq5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')

## 2000 - yield

data2000y = CSV.read("$datadir/spam_y.csv")
data = data2000y
data = data[data.stat_code .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[10:29]
X = Matrix(data[:,10:29])

##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
G = nngraph(idxs,dsts)

##
using DelimitedFiles
writeSMAT("cropsim-2000-yield.smat",G)
writedlm("cropsim-2000-yield.xy", zip(data.x,data.y))
##
# hc_seq5m is the same as cell5m in later datasets
writedlm("cropsim-2000-yield-metadata.csv",
    zip(data.alloc_key, data.hc_seq5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')


## 2005 - harvested area
# crops = names(data)[10:51]
data2005h = CSV.read("$datadir/spam2005V3r2_global_H_TA.csv")
data = data2005h
## This data doesn't have x,y so we add them.
"""
CELL5M is a 5-minute arc resolution view of the -180,-90
lat-long system. This corresponds to a cell-size of
0.08333333333. The following code converts between cell5m
values and latlong.
"""
function cell5m_to_latlong(cell::Int)
  nrows = 4320
  ncols = 2160
  col, row = divrem(cell, nrows)
  x = row*0.0833333333333333333-(180-0.0833333333333333333/2)
  y = (90-0.0833333333333333333/2) - col*0.0833333333333333333
  return x,y
end
function add_xy_coords!(df)
  cell5m = df.cell5m
  x = zeros(length(cell5m))
  y = copy(x)
  for i=1:length(cell5m)
    x[i],y[i] = cell5m_to_latlong(cell5m[i])
  end
  df.x = x
  df.y = y
end
add_xy_coords!(data)
data = data[data.iso3 .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[8:49]
X = Matrix(data[:,8:49])

##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
G = nngraph(idxs,dsts)
##
using DelimitedFiles
writeSMAT("cropsim-2005-harvestarea.smat",G)
writedlm("cropsim-2005-harvestarea.xy", zip(data.x,data.y))
##
using LinearAlgebra
writedlm("cropsim-2005-harvestarea-metadata.csv",
    zip(data.alloc_key, data.cell5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')


## 2005 - yield
data2005y = CSV.read("$datadir/spam2005V3r2_global_Y_TA.csv")
data = data2005y
add_xy_coords!(data)
data = data[data.iso3 .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[8:49]
X = Matrix(data[:,8:49])

##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
G = nngraph(idxs,dsts)
##
using DelimitedFiles
using LinearAlgebra

writeSMAT("cropsim-2005-yield.smat",G)
writedlm("cropsim-2005-yield.xy", zip(data.x,data.y))
writedlm("cropsim-2005-yield-metadata.csv",
    zip(data.alloc_key, data.cell5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')

## 2010 - harvested area
# crops = names(data)[10:51]
data2010h = CSV.read("$datadir/spam2010V1r1_global_H_TA.csv")
##
data = data2010h
data = data[data.iso3 .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[10:51]
X = Matrix(data[:,10:51])

##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
G = nngraph(idxs,dsts)
##
using DelimitedFiles
using LinearAlgebra

writeSMAT("cropsim-2010-harvestarea.smat",G)
writedlm("cropsim-2010-harvestarea.xy", zip(data.x,data.y))
writedlm("cropsim-2010-harvestarea-metadata.csv",
    zip(data.alloc_key, data.cell5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')


## 2010 - yield
data2010y = CSV.read("$datadir/spam2010V1r1_global_Y_TA.csv")
##
data = data2010y
data = data[data.iso3 .== "USA",:]
# filter out hawaii & alaska...
data=data[data.x .>= -140,:]
crops = names(data)[10:51]
X = Matrix(data[:,10:51])

##
include("nn.jl")
Y = copy(X')
@time idxs,dsts = nnsimple(Y,25)
G = nngraph(idxs,dsts)
##
using DelimitedFiles
using LinearAlgebra

writeSMAT("cropsim-2010-yield.smat",G)
writedlm("cropsim-2010-yield.xy", zip(data.x,data.y))
writedlm("cropsim-2010-yield-metadata.csv",
    zip(data.alloc_key, data.cell5m, sum.(eachrow(X)), norm.(eachrow(X)), maximum.(eachrow(X))), ',')
