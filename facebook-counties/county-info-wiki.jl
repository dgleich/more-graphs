## Get county info
using JSON
##
mapdata = JSON.parsefile("final-map.json")
counties = mapdata["objects"]["counties"]["geometries"]
## Get the county names
names = [String(counties[i]["properties"]["NAME"]) for i in eachindex(counties)]
stateid = [String(counties[i]["properties"]["STATEFP"]) for i in eachindex(counties)]
geoids = [String(counties[i]["properties"]["GEOID"]) for i in eachindex(counties)]

## Get county info from wikipedia
## https://en.wikipedia.org/wiki/User:Michael_J/County_table
data = String(read("wikipedia-county-info.txt"))
info = split(data,"|-\n")[3:end]

##
info_geoids = []
for line in info
  parts = split(chomp(line), "||")
  @assert(length(parts) == 14)
  geoid = split(parts[3], "|")[2]
  push!(info_geoids, geoid)
  name = split(parts[4], "|")[2]
  if !(geoid in geoids)
    println("Missing $(geoid) $(name)")
  end

  population = parse(Int,replace(split(parts[6], "|")[2], ","=>""))
  area = parse(Float64,replace(split(parts[12], "|")[2], ","=>""))
  long = parse(Float64, split(parts[13], "|")[2][1:end-1])
  # this must use an emdash – vs. - (yes, there is a difference there!)
  lat = parse(Float64, replace(split(parts[14], "|")[2][1:end-1], "–" => "-"))
end
## Check which we don't have info on
for geoid in geoids
  if !(geoid in info_geoids)
    println("Missing info on $(geoid)")
  end
end

## We are missing data on one county, let's just add it.
# Missing info on 02158
names[findfirst(geoids .== "02158")]
# Oh! This was just renamed...
# https://github.com/walkerke/tidycensus/blob/master/R/estimates.R
# Account for change from Shannon County, SD to Oglala Lakota County
# and the new Kusilvak Census Area in AK
# geom$GEOID[geom$GEOID == "46113"] <- "46102"
# geom$GEOID[geom$GEOID == "02270"] <- "02158"

## So we have everything!
##
info_geoids = []
info_population = zeros(Int,0)
info_area = zeros(0)
info_lat = zeros(0)
info_long = zeros(0)
info_state = Vector{String}()
info_name = Vector{String}()
for line in info
  parts = split(chomp(line), "||")
  @assert(length(parts) == 14)
  geoid = split(parts[3], "|")[2]
  name = split(parts[4], "|")[2]
  stateid = split(parts[2], "|")[3][1:2]
  if geoid == "02270" # see notes above
    geoid = "02158"
  end


  population = parse(Int,replace(split(parts[6], "|")[2], ","=>""))
  area = parse(Float64,replace(split(parts[12], "|")[2], ","=>""))
  long = parse(Float64, split(parts[13], "|")[2][1:end-1])
  # this must use an emdash – vs. - (yes, there is a difference there!)
  lat = parse(Float64, replace(split(parts[14], "|")[2][1:end-1], "–" => "-"))


  push!(info_name, name)
  push!(info_state, stateid)
  push!(info_lat, lat)
  push!(info_long, long)
  push!(info_area, area)
  push!(info_population, population)
  push!(info_geoids, geoid)
end

## Spit out metadata
# we want two files: xy coords with the lat/long
# -metadata.csv with the population and area
# build the permutation
rows = zeros(Int,0)
for g in geoids
  push!(rows, findfirst(info_geoids .== g))
end
## join state and name
names_states = names .* ", ".*info_state[rows]
## Quick verifyication of data
[info_name[rows][1:10] names_states[1:10]]
## Adjust the lat-long
xy = [info_lat[rows] info_long[rows]]
xy[9,1] = -180-(180-xy[9,1])

##
using DelimitedFiles
writedlm("facebook-county-friendship.xy", xy)
writedlm("facebook-county-friendship.labels", names_states)
writedlm("facebook-county-friendship-metadata.csv",
  zip(info_population[rows], info_area[rows], info_state[rows]))
