##
using Random, LinearAlgebra
Random.seed!(0)
X1 = randn(4,10)
DX = zeros(size(X1,2),size(X1,2))
for i=1:size(X1,2)
  for j=1:size(X1,2)
    DX[i,j] = norm(X1[:,i]-X1[:,j])
  end
end
##
function nnsimple(X,k)
  m,n = size(X)
  idxs = zeros(Int,k,n)
  dsts = zeros(Float64,k,n)
  d = zeros(n)
  ix = ones(Int,n)
  subset = 1:k
  @inbounds for i=1:n
    fill!(d,0)
    for j=1:n
      @simd for k=1:m
        d[j] += (X[k,i] - X[k,j])^2
      end
      d[j] = sqrt(d[j])
    end
    partialsortperm!(ix,d,subset);
    for j=1:k
      idxs[j,i] = ix[j]
      dsts[j,i] = d[ix[j]]
    end
  end
  return idxs,dsts
end
begin
  idxs,dsts = nnsimple(X1,10)
  for i=1:size(X1,2)
    @assert dsts[:,i] ≈ sort(DX[:,i])
  end
end
using SparseArrays
function nngraph(idxs::Matrix{T},dsts::Matrix{F}) where {T <: Integer, F <: Real}
  n = size(idxs, 2)
  ei = zeros(Int,0)
  ej = copy(ei)
  ev = zeros(Float64,0)
  for i=1:n
    for k=1:size(idxs,1)
      if i != idxs[k,i]
        push!(ei, i)
        push!(ej, idxs[k,i])
        push!(ev, dsts[k,i])

        push!(ei, idxs[k,i])
        push!(ej, i)
        push!(ev, dsts[k,i])
      end
    end
  end
  A = sparse(ei,ej,ev,n,n,max)
end
