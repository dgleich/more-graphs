##
using Shapefile
path = "/p/mnt/data/raw-data/megaregions/us_ttw_v3_US_only_epsg5070v2.shp"
table = Shapefile.Table(path)

## get the nodes and edges
tracts = unique(vcat(table.Ofips, table.Dfips))
tract2ind = Dict(tracts .=> 1:length(tracts))

src = map(i->tract2ind[i],table.Ofips)
dst = map(i->tract2ind[i],table.Dfips)


## commutes.net has the edge
# 71785 4122 1.000000
# 71785 8371 0.285714
# which map to
# 4122 "48323950500"
# 8371 "48507950301"
# 71785 "48507950200"
# we have
#=
julia> tract2ind["48507950200"]
69521

julia> tract2ind["48507950301"]
41675

julia> tract2ind["48323950500"]
6193

Which maps to the edge weight ESTDIVMOE
(exept, not... it's Flow./Moe)
=#


## get the coordinates
# lots of issues in getting this stuff, but they were all worked out
# and the following code s
function getxy(table)
  tract2xy = Dict{String,Tuple{Float64,Float64}}()
  Ofips = table.Ofips
  Dfips = table.Dfips
  for (i,geom) in enumerate(Shapefile.shapes(table))
    fsrc::String = Ofips[i]
    fdst::String = Dfips[i]
    @assert(length(geom.points) == 2)
    srcxy = (geom.points[1].x,geom.points[1].y)
    dstxy = (geom.points[2].x,geom.points[2].y)

    if haskey(tract2xy, fsrc)
      @assert srcxy == tract2xy[fsrc]
    else
      tract2xy[fsrc] = srcxy
    end

    if haskey(tract2xy, fdst)
      @assert dstxy == tract2xy[fdst]
    else
      tract2xy[fdst] = dstxy
    end
  end
  return tract2xy
end
tract2xy= getxy(table)

##
tracts_xy = map(i->tract2xy[i],tracts)
xy = [map(first, tracts_xy) map(i->i[2], tracts_xy)]
##
using SparseArrays
A = sparse(src, dst, table.Flow./table.Moe, length(tracts), length(tracts))
##
using MatrixNetworks
is_connected(A) # it isn't... we'll output largest cc below
## From https://github.com/dgleich/DGFun.jl/blob/master/src/io.jl
using DelimitedFiles
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
##
A32 = Float32.(A)
writeSMAT("commutes-all.smat", A32)
writedlm("commutes-all.xy.epsg5070", xy)
writedlm("commutes-all.labels", tracts)
##

## Let's also get the lat-long
# curl https://www2.census.gov/geo/docs/reference/cenpop2010/tract/CenPop2010_Mean_TR.txt -O
using CSV
ctracts = CSV.read("CenPop2010_Mean_TR.txt")
##
using Printf
cids = map(i->@sprintf("%02i",i), ctracts.STATEFP) .* map(i->@sprintf("%03i",i), ctracts.COUNTYFP) .* map(i->@sprintf("%06i",i), ctracts.TRACTCE)
##
cids2row = Dict(cids .=> 1:length(cids))
all(map(i->haskey(cids2row,i), tracts))
##
xyll = [ctracts.LONGITUDE[map(i->cids2row[i], tracts)] ctracts.LATITUDE[map(i->cids2row[i], tracts)]]
writedlm("commutes-all.xy", xyll)


## This is no longer used...
## Let's also output the connected network

#=
Acc,p = largest_component(A)
writeSMAT("commutes-scc.smat", Acc)
writedlm("commutes-scc.xy.epsg5070", xy[p,:])
writedlm("commutes-scc.labels", tracts[p])
writedlm("commutes-scc.xy", xyll[p,:])
=#
