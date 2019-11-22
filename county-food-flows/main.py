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

#mapping nodes and using fips name
#manually added a few entries in sorted order to file
#data for file obtained psuedo manually from https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt
#it was corrected via info at https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html
#08014 Broomfield County
#12086 Miami-Dade County
#46102 Oglala Lakota County

cpath= r'counties.txt'
reader = csv.reader(open(cpath,'r'))
newData = dict()
for item in reader:
    if item[0][-3:]=='000':
        state = item[1]
    else:
        newData[item[0]]=item[1]+','+' '+state
        
nodeMap = {nodes[k]:k for k in range(len(nodes))}

edges=list(map(lambda x:(nodeMap[x[0]],nodeMap[x[1]]),edges))

symEdges = set()
for k in edges:
    symEdges.add(k)
    symEdges.add((k[1],k[0]))        

#writing files
with open('counties.labels','w') as fptr:
    for k,item in enumerate([(nodes[k],newData[nodes[k]]) for k in range(len(nodes))]):
        fptr.write('{0:s}\t{1:s}\n'.format(item[0],item[1]))
    
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
    
