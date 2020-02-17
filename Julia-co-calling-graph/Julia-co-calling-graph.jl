using Pkg.Pkg.TOML
using Printf

# directory where Julia packages are stored
pkg_dir = "/Users/vaastavarora/.julia/packages/"

# this variable needs to be changed based on your own installation directory
path = "/Users/vaastavarora/.juliapro/JuliaPro_v1.2.0-2/registries/JuliaPro"
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

    # parse source file
    try
        src_expr = Meta.parse(src)
    catch err
        println("Error in file ",index,"/",length(std_pkg_names))
    end

    return src_expr
end

# Function for graph construction
function build_graph(exp::Expr)

    if exp.head == Symbol(":function")
        if size(exp.args)>2
            throw(Exception)
        end


        if exp.args[1] in found_functions
            Nothing
        else
            push!(found_functions,exp.args[1])
            function_graph[exp.args[1]] = []
        end
    else
        for texp in exp.args
            if typeof(texp) == Expr
                build_graph(texp)
            end
        end
    end
end

# Iterate all files in std package
for i = 1:length(std_pkg_names)
    exps = resolve_path(i)
    build_graph(exps)
end


## TODO
# Fix symbol matching for functions
# Map invoke/calls from within function
# build co-calling graph
