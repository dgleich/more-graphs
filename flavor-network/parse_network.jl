# parse the networks
using CSV
data = CSV.read("srep00196-s2.csv",comment="#")
##
allcompounds = [data[:,1]; data[:,2]]
##
@show length(unique(data[:,1]))
@show length(unique(data[:,2]))
@show length(unique(allcompounds))
## Build a sparse matrix out of this data
using CategoricalArrays
##
using SparseArrays
x=CategoricalArray(allcompounds,ordered=false)
allingreds = levels(x)
ids = Int.(CategoricalArrays.order(x.pool)[x.refs])
src = ids[1:size(data,1)]
dst = ids[size(data,1)+1:end]
A = sparse(src,dst,data[:,3],length(allingreds),length(allingreds))
## A is only upper-triangular
using LinearAlgebra
@assert(iszero(A-triu(A,1)))
A = max.(A,A')
##
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
writeSMAT("ingredient-net.smat", Int.(sparse(A)))

##
using DelimitedFiles
writedlm("ingredient-net.labels", allingreds)

##
# build the id map
ingred2id = Dict(allingreds .=> 1:length(allingreds))
##
recipes = readlines("srep00196-s3.csv")
ingred = Vector{Vector{String}}(undef,0)
cusines = Vector{String}(undef,0)
for line in recipes
  if startswith(line, "#")
    continue
  else
    parts = split(line, ",")
    push!(cusines, parts[1])
    push!(ingred, collect(parts[2:end]))
  end
end


## map to indices
# we are missing startch and condiment
recipes = [[ingred2id[x] for x in recipe if (x != "starch" && x != "condiment")]
              for recipe in ingred]
R = sparse(collect(Iterators.flatten([r*ones(Int,length(recipes[r])) for r in 1:length(recipes)])),
           collect(Iterators.flatten(recipes)),1)
##
writeSMAT("recipes.smat", R)
##
writedlm("recipes.labels", cusines)
