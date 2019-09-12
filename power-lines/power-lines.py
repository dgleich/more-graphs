import scipy.sparse as sp
import pandas as pd

df_power_lines = pd.read_csv("Electric_Power_Transmission_Lines.csv")
# convert names into upper case
stations_candidates1 = set([s.upper() for s in list(set(df_power_lines["SUB_1"].values.tolist()+df_power_lines["SUB_2"].values.tolist()))])
# "NONE" is not considered as a legal name 
if "NONE" in stations_candidates1:
    stations_candidates1.remove("NONE")

# same procedure repeated for the metadata file
df_stations = pd.read_csv("Electric_Substations.csv")
stations_candidates2 = {s.upper():i for i,s in enumerate(df_stations["NAME"].values)}
if "NONE" in stations_candidates2:
    stations_candidates2.remove("NONE")

#filtered out stations where we don't have metadata
stations = list(stations_candidates1.intersection(stations_candidates2.keys()))
stations_map = {stations[i]:i for i in range(len(stations))}

wptr = open("power-lines.labels","w")
for station in stations:
    wptr.write(station+"\n")
wptr.close()

wptr = open("power-lines.xy","w")
for station in stations:
    X,Y = df_stations.iloc[stations_candidates2[station]]["X"],df_stations.iloc[stations_candidates2[station]]["Y"]
    wptr.write("{0:f}\t{1:f}\n".format(X,Y))
wptr.close()

ei,ej,e = [],[],[]
for i in range(df_power_lines.shape[0]):
    si,sj = df_power_lines.iloc[i]["SUB_1"],df_power_lines.iloc[i]["SUB_2"]
    if si in stations_map and sj in stations_map:
        ei.append(stations_map[si])
        ej.append(stations_map[sj])
        e.append(1)

G = sp.csr_matrix((e,(ei,ej)),shape=(len(stations),len(stations)))
sel = G.T > G
G = G - G.multiply(sel) + G.T.multiply(sel)

ei = G.tocoo().row
ej = G.tocoo().col
e = G.tocoo().data

wptr = open("power-lines.smat","w")
wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(len(stations),len(stations),len(ei)))
for i in range(len(ei)):
    wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(ei[i],ej[i],e[i]))
wptr.close()