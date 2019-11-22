####uses supplementary data provided from 
#https://iopscience.iop.org/article/10.1088/1748-9326/ab29ae#supplementarydata


#remeber to cite the paper!
import csv

edges = set()
nodes = set()

fpath = r'erl_14_8_084011_sd_3.csv'

with open(fpath,'r') as fptr:
    reader = csv.reader(fptr)
    header = next(reader)
    
    srcInd = header.index('ori')
    dstInd = header.index('des')
    
    for line in reader:
        src = line[srcInd]
        dst = line[dstInd]
        edges.add((src,dst))
        nodes.add(src)
        nodes.add(dst)
        
nodes = list(nodes)
nodes.sort()
 
nodeMap = {nodes[k]:k for k in range(len(nodes))}
edges=list(map(lambda x:(nodeMap[x[0]],nodeMap[x[1]]),edges))

symEdges = set()
for k in edges:
    symEdges.add(k)
    symEdges.add((k[1],k[0]))        


#requires data from https://github.com/dgleich/more-graphs/tree/master/misc-county-fips-data
#which contains same data as 
tab = dict()
with open('county-data.txt','r',encoding='utf-8') as fptr:
    reader = csv.reader(fptr,delimiter='\t')
    header = next(reader)
    stateInd = header.index('state')
    fipsInd = header.index('fips')
    countyInd = header.index('county')
    latInd = header.index('latitude')
    lonInd = header.index('longitude')
    
    for item in reader:
        tab[item[fipsInd]] = [item[countyInd]+', '+item[stateInd],item[latInd],item[lonInd]]


#writing files
with open('counties.labels','w',encoding='utf-8') as fptr:
    for item in [(nodes[k],tab[nodes[k]][0]) for k in range(len(nodes))]:
        fptr.write('{0:s}\t{1:s}\n'.format(item[0],item[1]))
    
#this needs file found at     
with open('counties.xy','w',encoding='utf-8') as fptr:
    for item in [tab[nodes[k]][1:] for k in range(len(nodes))]:
        fptr.write('{0:s}\t{1:s}\n'.format(item[0],item[1]))
    
with open('full-county-info.xy','w',encoding='utf-8') as fptr:
    for k in nodes:
        fptr.write('{0:s}\t{1:s}\t{2:s}\t{3:s}\n'.format(k,tab[k][0],tab[k][1],tab[k][2]))
    
edges.sort()

with open('dir-county-flows.smat','w') as fptr:    
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(len(nodes),len(nodes),len(edges)))
    for item in edges:
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(item[0],item[1],1))

symEdges = sorted(symEdges)
with open('undir-county-flows.smat','w') as fptr:    
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(len(nodes),len(nodes),len(symEdges)))
    for item in symEdges:
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(item[0],item[1],1))
