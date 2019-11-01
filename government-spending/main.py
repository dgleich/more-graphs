'''DATA obtained from: https://www.usaspending.gov/#/download_center/award_data_archive 
 for the 2018 fiscal year of the contracts files
 
 Data was obtained on 09-18-2019
 
 
 TODO: organize and clean up
'''

import os,csv,gc
import sqlite3 as sql
gc.enable()


###BUILDING SQL DATABASE AND CORRECTING THE DATA
path = r'C:\Users\Omar\Desktop\Contracts'
os.chdir(path)
originalFilePath = r'2018_all_Contracts_Full_20190911'
deltaFilePath = r'all_Contracts_Delta_20190911'

#make SQL database and initialize table
con = sql.connect('2018-gov-spending.db')
cur = con.cursor()

#reading data, chunks at a time and inserting into table
os.chdir(originalFilePath)
data = []
for i,file in enumerate(os.listdir()):
    print('working on file '+str(i+1)+' of '+str(len(os.listdir() )))
    with open(file,'r',encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=',')
        header = next(csvreader) #make header and extract relevant info
        
        info = ['contract_transaction_unique_key','funding_agency_code','funding_agency_name',
                'funding_sub_agency_code','funding_sub_agency_name','recipient_duns','recipient_name',
                'recipient_parent_name','recipient_parent_duns']
        inds = list(map(lambda x: header.index(x),info))
        
        insertCommand = 'INSERT INTO spending VALUES ('+'?,'*len(info)
        insertCommand = insertCommand[:-1]+');' 
        
        if i==0:
            tabCommand = 'CREATE TABLE IF NOT EXISTS spending ('
            tabCommand += ' text, '.join(map(lambda x: '"'+x+'"',info))
            tabCommand += ' text)'
            
            cur.execute(tabCommand)
            
        for line in csvreader:
            if len(data)%100000==0 and len(data)>0:
                cur.executemany(insertCommand,data)
                data = []
            
            data.append(tuple([line[ind] for ind in inds]))

cur.executemany(insertCommand,data)
con.commit()
            
                        
#creating index
sqlCommand = 'CREATE UNIQUE INDEX idx ON spending("contract_transaction_unique_key")'
cur.execute(sqlCommand)


#using delta files to update errors
os.chdir('..')
os.chdir(deltaFilePath)
for i,file in enumerate(os.listdir()):
    print('working on file '+str(i+1)+' of '+str(len(os.listdir() )))
    with open(file,'r',encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=',')
        deltaHeader = next(csvreader) #make header once and extract relevant info
        
        deltaInds = list(map(lambda x: deltaHeader.index(x),info))
        
        yearInd = deltaHeader.index('action_date_fiscal_year')
        
        replaceCommand = 'REPLACE INTO spending VALUES('+'?,'*(len(info))
        replaceCommand = replaceCommand[:-1]+');' 
        
        deleteCommand = 'DELETE FROM spending WHERE contract_transaction_unique_key='
        
        
        for line in csvreader:
            if line[yearInd]=='2018':    
                if line[0].lower() in ['c','']: #replace/insert in db
                    cur.execute(replaceCommand,tuple([line[ind] for ind in deltaInds]))
                elif line[0].lower()=='d':
                    cur.execute(deleteCommand+'"{}"'.format([line[ind] for ind in deltaInds]))
con.commit()
                
os.chdir('..')



#### BUILDING GRAPHS
recipientNameInd = info.index('recipient_name')
recipientDUNS_Ind = info.index('recipient_duns')

parentNameInd = info.index('recipient_parent_name')
parentDUNS_Ind = info.index('recipient_parent_duns')
    
fundingAgencyNameInd = info.index('funding_agency_name')
fundingAgencyCodeInd = info.index('funding_agency_code')

fundingSubAgencyNameInd = info.index('funding_sub_agency_name')
fundingSubAgencyCodeInd = info.index('funding_sub_agency_code')

#initializing 
edges = set()
recipientInfo = set() #DUNS:name
funding = dict() 

data = cur.execute('SELECT * FROM spending')

#builid edges
for i,line in enumerate(data):
    recipient = line[recipientDUNS_Ind]
    recipientName = line[recipientNameInd]
        
    parent = line[parentDUNS_Ind]
    parentName = line[parentNameInd]
        
    fundingAgency = line[fundingAgencyCodeInd]
    fundingAgencyName = line[fundingAgencyNameInd]
    fundingSubAgency = line[fundingSubAgencyCodeInd]
    fundingSubAgencyName = line[fundingSubAgencyNameInd]
        
    if '' not in [recipient,recipientName,fundingAgency,fundingAgencyName,
                  fundingSubAgency,fundingSubAgencyName]:
        
        funder = fundingAgency+'||'+fundingSubAgency#+'||'+fundingOffice
        funderName = fundingAgencyName+'||'+fundingSubAgencyName#+'||'+fundingOfficeName
        
        if parent!='': #this field is nonempty so use parent info
            edges.add((parent,funder))    
            recipientInfo.add((parent,parentName))
            
        else: #have to use recipient info
            edges.add((recipient,funder))                
            recipientInfo.add((recipient,recipientName))
            
        #other data
        if funder not in funding:
            funding[funder] = funderName

### hashing edges
companyNames = dict(recipientInfo)
govNames = dict(funding)

govMap = {gname:k for k,gname in enumerate(govNames)}
companyMap = {cname:k + len(govMap) for k,cname in enumerate(companyNames)}

hashedGovNames = {govMap[k]:govNames[k] for k in govMap}
hashedCompanyNames = {companyMap[k]:companyNames[k] for k in companyMap}

nnodes = len(govMap)+len(companyMap)

with open('subagencies.labels','w') as fptr:
    for k in sorted(hashedGovNames.keys()):
        fptr.write('%s\n' %(hashedGovNames[k]))

with open('companies.labels','w') as fptr:
    for k in sorted(hashedCompanyNames.keys()):
        fptr.write('%s\n' %(hashedCompanyNames[k]))

hashedEdges = list(map(lambda x:(companyMap[x[0]],govMap[x[1]]),edges))
hashedEdges+=list(map(lambda x: (x[1],x[0]),hashedEdges))
nedges = len(hashedEdges)

with open('contracts-edges.smat','w') as fptr:
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(nnodes,nnodes,nedges))
    for e in sorted(hashedEdges):
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(e[0],e[1],1))