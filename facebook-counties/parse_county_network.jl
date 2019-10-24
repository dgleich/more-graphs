function load_friends()
  buf = open("county2county.binary") do io
    read(io)
  end
  len = length(buf)
  n = Int.(sqrt(len*2))
  @assert n == 3142
  X = zeros(n,n)
  # each entry is encoded in 4 bits
  for i=1:n
    for j=1:2:n # each
      byteno = (((i-1)*n) + (j-1)) ÷ 2 + 1
      byte = buf[byteno]
      X[j,i] = (byte & 0b11110000) >> 4
      X[j+1,i] = (byte & 0b1111)
    end
  end
  return X
end
X = load_friends()

## From the Chrome Debugger

Y = [0 8
1 7
2 8
3 8
4 7
5 8
6 8
7 7
8 8
9 7
10 8
11 7
12 8
13 7
14 7
15 8
16 7
17 8
18 8
19 8
20 8
21 7
22 7
23 8
24 7
25 8
26 7
27 7
28 7
29 7
30 7
31 7
32 7
33 7
34 8
35 6
36 8
37 7
38 7
39 7
40 8
41 7
42 8
43 8
44 7
45 8
46 7
47 7
48 7
49 8
50 8
51 7
52 8
53 7
54 8
55 7
56 7
57 7
58 8
59 8
60 8
61 8
62 8
63 7
64 7
65 8
66 7
67 1
68 1
69 4
70 1
71 2
72 4
73 1
74 4
75 1
76 1
77 1
78 3
79 2
80 2
81 1
82 1
83 2
84 1
85 3
86 1
87 4
88 1
89 2
90 2
91 2
92 1
93 1
94 4
95 1
96 1
97 2
98 1
99 1]
for i=1:size(Y,1)
  @assert(Y[i,2].== X[i,1])
end
## The smallest value is X
minimum(X)

## the smallest entry
A = X .- 1

## There are 1818 non-symmetric entries
nonsym = findall(abs.(A-A') .> 0)
display(nonsym)
## Let's look at them
for i=1:50
  println("A[$(nonsym[i])] = $(A[nonsym[i]]) ≠ $(A[nonsym[i][2],nonsym[i][1]])")
end
## Is the difference always at most one?

diffs = [ abs(A[nonsym[i]] - A[nonsym[i][2],nonsym[i][1]]) for i in eachindex(nonsym)]

## Ugh, there are 8 entries where the differnce is larger than 1
count(diffs .> 1)

##
nonsym[findall(diffs .> 1)]

##
diffs[findall(diffs .> 1)]
## We are going to symmetrize this and have a list of corrections.
B = min.(A,A') # this is the strenght of both...
C = A - B # this is the correction

## From https://github.com/dgleich/DGFun.jl/blob/master/src/io.jl
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
writeSMAT("facebook-county-friendship.smat", Int.(sparse(B)))
writeSMAT("facebook-county-friendship-nonsym.smat", Int.(sparse(C)))

##
## Let's also parse the top-10 network
using DelimitedFiles
topdata = Int.(readdlm("top.csv",',',skipstart=1))
##
T = sparse(topdata[:,1] .+ 1,topdata[:,2] .+ 1,1, 3142,3142 )
##
writeSMAT("facebook-county-friendship-top10.smat", T)
