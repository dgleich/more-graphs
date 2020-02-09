
##
"""
CELL5M is a 5-minute arc resolution view of the -180,-90
lat-long system. This corresponds to a cell-size of
0.08333333333. The following code converts between cell5m
values and latlong.
"""
function cell5m_to_latlong(cell::Int)
  nrows = 4320
  ncols = 2160
  col, row = divrem(cell, nrows)
  x = row*0.0833333333333333333-(180-0.0833333333333333333/2)
  y = (90-0.0833333333333333333/2) - col*0.0833333333333333333
  return x,y
end
cell5m_to_latlong(1300706)
## Test data (from spam2010V1r1_global_H_TA)

cell5m_test = [1300706
1300707
1300708
1305026
1305027
1305028
1348258
1348259
1348260
1352579
1352580
1473490]
cell5m_ref_x = [-147.7916666668
-147.7083333335
-147.6250000001
-147.7916666668
-147.7083333335
-147.6250000001
-145.1250000001
-145.0416666668
-144.9583333335
-145.0416666668
-144.9583333335
-149.1250000001]
cell5m_ref_y = [ 64.8749999994
 64.8749999994
 64.8749999994
 64.791666666
 64.791666666
 64.791666666
 63.9583333327
 63.9583333327
 63.9583333327
 63.8749999994
 63.8749999994
 61.5416666661]
for i in 1:length(cell5m_test)
  x,y = cell5m_to_latlong(cell5m_test[i])
  println(cell5m_test[i], " ",
          x, " ", cell5m_ref_x[i], " ",
          y, " ", cell5m_ref_y[i])
  @assert (x ≈ cell5m_ref_x[i])
  @assert (y ≈ cell5m_ref_y[i])
end
##
