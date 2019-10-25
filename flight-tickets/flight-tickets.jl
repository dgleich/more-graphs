using Plots
using GraphRecipes
using CSV

tickets_df = CSV.read("833829401_T_DB1B_MARKET.csv")

coords_df = CSV.read("833829401_T_MASTER_CORD.csv")

US_airports = coords_df[coords_df.AIRPORT_COUNTRY_NAME .== "United States",:]

y = Array{Float64}(collect(US_airports[:LATITUDE])[1:(end-1)])

x = Array{Float64}(collect(US_airports[:LONGITUDE])[1:(end-1)])

tmp = findall(x.>0)
x[tmp] = x[tmp] .- 360

US_tickets = tickets_df[(tickets_df.ORIGIN_COUNTRY .== "US") .& (tickets_df.DEST_COUNTRY .== "US"),:]

US_airports_ids = US_airports[:AIRPORT_ID][1:(end-1)]
US_airports_ids_mapping = Dict(US_airports_ids[i]=>i for i in 1:length(US_airports_ids))
US_tickets_src = US_tickets[:ORIGIN_AIRPORT_ID]
US_tickets_dst = US_tickets[:DEST_AIRPORT_ID]

src,dst = Int64[],Int64[]
for i in 1:length(US_tickets_src)
    push!(src,US_airports_ids_mapping[US_tickets_src[i]])
    push!(dst,US_airports_ids_mapping[US_tickets_dst[i]])
    # convert each edge to undirected
    push!(dst,US_airports_ids_mapping[US_tickets_src[i]])
    push!(src,US_airports_ids_mapping[US_tickets_dst[i]])
end

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

A = sparse(src,dst,ones(length(src)),length(x),length(x))
writeSMAT("flight-tickets.smat",A)

xy = hcat(x,y)

using DelimitedFiles
writedlm("us-airports.xy", xy)
writedlm("us-airports.labels", US_airports[:DISPLAY_AIRPORT_NAME][1:(end-1)])
writedlm("us-airports-metadata.csv",
  zip(US_airports[:AIRPORT_ID][1:(end-1)], US_airports[:AIRPORT_STATE_NAME][1:(end-1)], US_airports[:CITY_MARKET_ID][1:(end-1)]))
