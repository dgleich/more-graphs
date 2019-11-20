### FOOD FLOWS NETWORK CREATION

#data obtained from: https://www.census.gov/data/datasets/2012/econ/cfs/2012-pums-files.html
#note data has been anonymized and noise has been added

#this is for u.s. national food flow data (excluding exports)

import os
import csv
import openpyxl


fpath =  r'C:\Users\Omar\Desktop\food-flow-data'
os.chdir(fpath)

#node names for later
wb = openpyxl.load_workbook('cfs-2012-pum-file-users-guide-app-a-jun2015.xlsx')
sheet = wb.get_sheet_by_name('App A1') #relevant data is A,B,E 4:136. code: B-A name E
codes = sheet['A4':'B136']
names = sheet['E4':'E136']

node_codes = []
for row in codes:
    node_codes.append(str(row[1].value)+'-'+str(row[0].value))

node_names = []
for row in names:
    node_names.append(str(row[0].value))

#excel file appears to missing a single entry. it was manually added via consultation
#with the pdf available online, pg 8 the first entry of appendix A-1
name_map = {node_codes[k]:node_names[k] for k in range(len(node_codes))}
name_map['36-104']='Albany-Schenectady, NY CFS Area'

os.chdir('cfs-2012-pumf-csv')
file = os.listdir()[0] #only file in dir

edges = set()
nodes = set()
with open(file,'r') as fptr:
    data = csv.reader(fptr,delimiter=',')
    header = next(data)
    
    srcCodeInd = header.index('ORIG_CFS_AREA')
    dstCodeInd = header.index('DEST_CFS_AREA')
    shipmentSctgInd = header.index('SCTG')
    exportBoolInd = header.index('EXPORT_YN') 
    
    #admissible codes as well as possible errors 
    agricultureCodes = ['0'+str(i) for i in range(1,10)] + ['01-05','06-09'] 
    errs = [str(i) for i in range(1,10)]+['01-5','1-05','1-5','06-9','6-09','6-9']
    agricultureCodes += errs
        
    for record in data:        
        if record[exportBoolInd].lower()!='y':#domestic shipment
            src,dst = record[srcCodeInd],record[dstCodeInd]
            
            if src[-5:]!='00000' and dst[-5:]!='00000':#information was not concealed
                if record[shipmentSctgInd] in agricultureCodes: #right kind of flow
                    nodes.add(src)
                    nodes.add(dst)
                    edges.add((src,dst))
os.chdir('..')

#process nodes for smat file
nodes = sorted(nodes)
nodeHash = {nodes[k]:k for k in range(len(nodes))}

nodeMap = zip(map(lambda x:nodeHash[x],nodes),nodes,map(lambda x:name_map[x],nodes))

with open('locations.labels','w') as fptr:
    fptr.write('{0:s}\t{1:s}\t{2:s}\n'.format('node id','identifer in data','location'))
    for row in nodeMap:
        fptr.write('{0:d}\t{1:s}\t{2:s}\n'.format(row[0],row[1],row[2]))
    
#hash edges
sym_edges = set()
for e in edges:
    v1,v2 = nodeHash[e[0]],nodeHash[e[1]]
    sym_edges.add((v1,v2))
    sym_edges.add((v2,v1))
    
edges = list(map(lambda x: (nodeHash[x[0]],nodeHash[x[1]]),edges))

#write directed and undirected smat files
with open('dir-food-flows.smat','w') as fptr:
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(len(nodes),len(nodes),len(edges)))
    for e in sorted(edges):
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(e[0],e[1],1))
    
with open('food-flows.smat','w') as fptr:
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(len(nodes),len(nodes),len(sym_edges)))
    for e in sorted(sym_edges):
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(e[0],e[1],1))
    