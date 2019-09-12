using DelimitedFiles

# write_to_smat
function writeToSMAT(M,filename)
    #if unweighted
    if size(M,2) == 2
        M = hcat(M,ones(Int,size(M,1)))
    end
    m = maximum(M)+1
    nz = size(M,1)
    open(filename, "w") do f
        write(f, "$m   $m   $nz \n")
        writedlm(f,M)
    end
end
function findin_index(x,y)
     indices_in_y = zeros(Int64,length(x))
     already_exist = findall((in)(y), x)
     donot_exist = setdiff(1:length(x),already_exist)
     funcmap = i -> indices_in_y[findall(x.==y[i])] .= i
     lookfor_indices = findall((in)(x), y)
     map(funcmap,lookfor_indices)
     return indices_in_y
end

function run_script()
    M = readdlm("playerinfo.txt",header=true)
    names = M[1][:,3].*" ".*M[1][:,2]
    name_ids = M[1][:,1]
    names_data = hcat(name_ids,names)

    allfiles = readdir("pitcherinfo")
    myedge_list = Array{Int64}(undef,0,2)
    for i = 1:length(allfiles)
        fileid = allfiles[i]
        Mi = readdlm(joinpath("pitcherinfo",fileid))
        # 1(skip) - 20 - 1(skip) - 20 
        # the crawler needs to change to not crawl "pitcher" every 20 lines
        interestingids = findall(Mi[:,1].!="Pitcher")
        curfullnames = Mi[interestingids,1].*" ".*Mi[interestingids,2]
        indexnumbers = findin_index(curfullnames,names_data[:,2])
        connectto = indexnumbers[findall(indexnumbers.!=0)]
        curplayerid = fileid[1:findfirst("_",fileid)[1]-1]
        curplayerid_inlist = findfirst(name_ids.==curplayerid)
        new_connections = hcat(ones(Int64,length(connectto)).*curplayerid_inlist,connectto)
        myedge_list = vcat(myedge_list,new_connections)
    end
myedge_list.-=1
return myedge_list,names_data
end