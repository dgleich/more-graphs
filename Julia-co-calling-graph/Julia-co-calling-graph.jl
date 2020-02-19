using Pkg.Pkg.TOML
using Printf

# directory where Julia packages are stored
pkg_dir = "/Users/mengliu/.julia/packages/"

# this variable needs to be changed based on your own installation directory
path = "/Users/mengliu/.julia/registries/General"
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

# next, we use the first package as an example
std_pkg_names[1]

joinpath(STDLIB_DIR,std_pkg_names[1])

# grab the first source file
curr_path = joinpath(joinpath(STDLIB_DIR,std_pkg_names[1]),"src")
src_file = readdir(curr_path)[1]
curr_file = joinpath(curr_path,src_file)

# read source file as string
src = read(curr_file,String)

# parse source file
src_expr = Meta.parse(src)

# this function will go thourgh all the expressions in the source file
found_functions = Set()
function find_functions(expr::Union{GlobalRef,
    LineNumberNode,String,Symbol,Bool,QuoteNode},
    found_functions) end # do nothing
function find_functions(expr::Expr,found_functions)
    for arg in expr.args
        # expr.head will store which function is called in this expression
        if typeof(arg) == Expr
            push!(found_functions, expr.head)
        end
        find_functions(arg, found_functions)
    end
end

find_functions(src_expr,found_functions)

## TODO
# run find_functions on all source files of all packages
# build a mapping between all possible function names and node indices
# build co-calling graph
