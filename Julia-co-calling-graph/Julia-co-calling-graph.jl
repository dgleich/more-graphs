using Pkg.Pkg.TOML
using Printf

# directory where Julia packages are stored
pkg_dir = "/Users/vaastavarora/.julia/packages/"

# this variable needs to be changed based on your own installation directory
path = "/Users/vaastavarora/.julia/registries/General"
packages_dict = TOML.parsefile(joinpath(path,"Registry.toml"))["packages"]
# this variable needs to be changed based on your own installation directory
const STDLIB_DIR = "/Applications/Julia-1.3.app/Contents/Resources/julia/share/julia/stdlib/v1.3/"
const STDLIBS = readdir(STDLIB_DIR)

# find all Julia standard packages
std_pkg_names = []
for (i, stdlib) in enumerate(STDLIBS)
    if isfile(joinpath(STDLIB_DIR, stdlib, "Project.toml"))
        proj = TOML.parsefile(joinpath(STDLIB_DIR, stdlib, "Project.toml"))
        push!(std_pkg_names,proj["name"])
    end
end


# Set of functions found so far
found_functions = Set()
# Dictonary of functions with function prototype as key and storing their internal invocations as payload
function_graph = Dict()


# Function to resolve std package name
function resolve_path(index)
    joinpath(STDLIB_DIR,std_pkg_names[1])

    # grab the first source file
    curr_path = joinpath(joinpath(STDLIB_DIR,std_pkg_names[index]),"src")
    src_file = readdir(curr_path)[1]
    curr_file = joinpath(curr_path,src_file)

    # read source file as string
    src = read(curr_file,String)

    src_expr = Expr(:call, :+, 1, 1)

    # parse source file
    try
        src_expr = Meta.parse(src)
        return src_expr
    catch err
        println("Error in file ",index,"/",length(std_pkg_names))
        return Expr(:call, :+, 1, 1)
    end

end

prog = """
function nngraph(idxs::Matrix{Int32})
  n = size(idxs, 2)
  ei = zeros(Int,0)
  ej = copy(ei)
  for i=1:n
    for k=1:size(idxs,1)
      push!(ei, i)
      push!(ej, idxs[k,i])
    end
  end
  A = sparse(ei,ej,1.0,n,n)
  return max.(A,A')
end
"""

match_set = Set([Symbol("call"), Symbol(".")])
sets = []
# Function for graph construction
function build_graph(exp::Expr)

    println(exp.head)
    if exp.head == Symbol("function")
        println("Function Found")
        #print(size(exp.args))
        if size(exp.args)[1]>2
            throw(Exception)
        end

        t =  build_graph(exp.args[2])
        sets = [sets; t]
        return t

    elseif exp.head in match_set
        #println("found a call",exp.args[1])
        t = Set([exp.args[1]])

        for x in exp.args
            if typeof(x) == Expr
                println("about to call ",x," ",typeof(x))
                union!(t,build_graph(x))
            end
        end

        return t
    else
        t = Set()
        for texp in exp.args
            if typeof(texp) == Expr
                println("about to call ",texp," ",typeof(texp))
                union!(t,build_graph(texp))
            end
        end

        return t
    end
end


# Iterate all files in std package
for i = 1:length(std_pkg_names)
    exps = resolve_path(i)
    if typeof(exps) != Nothing
        println(exps)
        build_graph(exps)
    end
    #dump(exps)
end


## TODO
# Fix symbol matching for functions
# Map invoke/calls from within function
# build co-calling graph
