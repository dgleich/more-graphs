# Path: ./more-graphs/
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


data_dir = os.path.join(os.getcwd(), 'nsf-coaward', 'data')
output_dir = os.path.join(os.getcwd(), 'nsf-coaward')

#will build the following networks:
    # co-awards by year (researchers) #listed as "NSF_ID" in data
    # co-awards by year (university)  #listed as "ORG_UEI_NUM" in data
    # aggreagted co-awards for researchers
    # aggreagted co-awards for universities

#though somewhat verbose, variable names are chosen to coincide with names in the data

def fetch_data(tree_list,tag,backup_tag=None):
    """Fetch data from xml tree.
    
    Args:
        tree: xml tree
        tag: tag to search for
    Returns:
        data: list of data
    """
    if type(tree_list) == ET.ElementTree:
        tree_list = [tree_list]

    # institution_ids = [inst.findall('ORG_UEI_NUM') for inst in institutions]
    # if institution_ids == [[]]: #if no UEI, try DUNS
    #     institution_ids = [inst.findall('ORG_DUNS_NUM')[0].text for inst in institutions]
    # else:
    #     institution_ids = [inst[0].text for inst in institutions]        
    

    result = [tree.findall(tag) for tree in tree_list]
    if result == [[]] and backup_tag is not None:
        result = [tree.findall(backup_tag) for tree in tree_list]
    if result == [[]]:
        return None
    else: 
        return [x[0].text for x in result]


def process_file(filename):
    """Process a single award file.
    
    Args:
        filename: name of file to process
    Returns:
        incomplete: boolean indicating if file did not contain relevant data
        researchers: list of researchers
        institutions: list of institutions
        amount: amount of award        
    """
    false_output = False, [], [], 0
    if filename.endswith('.xml'):
        #get relevant data from file (researchers, institutions, amount)
        tree = ET.parse(filename)

        # get root element
        root = tree.getroot()

        #extract relevant data 
    
        award = root.findall('Award')[0]
        awardAmount = award.findall('AwardAmount')[0].text
        if awardAmount is None:
            return false_output
        #investigaor info
        investigators = award.findall('Investigator')
        
        investigator_ids = fetch_data(investigators,'NSF_ID')
        if investigator_ids is None:
            return false_output

        investigator_first_names = [inv.findall('FirstName')[0].text for inv in investigators]
        investigator_last_names = [inv.findall('LastName')[0].text for inv in investigators]

        #institution info
        institutions = award.findall('Institution')

        institution_names = [inst.findall('Name')[0].text for inst in institutions]
        #institution info can either be a 12 char unique entity identifier (UEI) or a 9 char DUNS number  
        institution_ids = fetch_data(institutions,'ORG_UEI_NUM','ORG_DUNS_NUM')


        #error checking
        if investigator_ids is None or investigator_ids is None:
            return false_output
        
        if len(investigator_ids)!=len(investigator_first_names)!=len(investigator_last_names):
            return false_output
        
        if len(institution_ids)!=len(institution_names):
            return false_output
        
        #prep output
        investigator_info = list(zip(investigator_first_names, investigator_last_names, investigator_ids))
        institution_info = list(zip(institution_names, institution_ids))

        return True, investigator_info, institution_info, awardAmount
    else:
        return false_output

#testing 
#older file 
xmlfile = 'nsf-coaward/data/1959/5900036.xml'
process_file(xmlfile)
## should return (False, [], [], 0)

#current file
xmlfile = 'nsf-coaward/data/2022/2200023.xml'
process_file(xmlfile)
## should return (True, [('Michelle', 'Wyman', '000803850')], [('National Council for Science and the Environment/CEDD', 'LLNMWDJVJ1Y9')], '59988')

#somewhere in the middle
xmlfile = 'nsf-coaward/data/2015/1566634.xml'
process_file(xmlfile)
## should return (True, [('Ming', 'Li', '000677955')], [('Board of Regents, NSHE, obo University of Nevada, Reno', '146515460')], '171892')

#checking one of davids
xmlfile = 'nsf-coaward/data/2011/1149756.xml'
process_file(xmlfile)
## should return (True, [('David', 'Gleich', '000596242')], [('Purdue University', 'YRXVL4JYCEF5')], '568943')

#process all files
data = []
nfiles = 0
for folder in os.listdir(data_dir):
    print("working on folder: ", folder, " with ", len(os.listdir(os.path.join(data_dir, folder))), " files")
    for file in os.listdir(os.path.join(data_dir, folder)):
        fname = os.path.join(data_dir, folder, file)
        nfiles += 1
        try:
            tmp = process_file(fname)
            if tmp[0]==True:
                data.append(tmp)
        except:
            pass


print("proportion of files processed: ",len(data)/nfiles)


#check for multiple institutions
c = 0
for award in data:
    data_bool, researcher_info, institution_info, amount = award
    if len(institution_info)>1:
        c+=1
print("number of awards with multiple institutions: ", c)
#found that files with multiple institutions were not present in the data which is strange..
#will ignore this for now and just build network for researchers only

#build edgelist for researchers
researcher_edgelist = defaultdict(int) # (src,dst): total weight
researchers = defaultdict(set) #key: researcher id, value: Set(researcher name(s))
for award in data:
    data_bool, researcher_info, institution_info, amount = award
    amount = int(amount) 
    if data_bool==True and award is not None and amount>0:
        #process researcher info
        if len(researcher_info)>1:
            for i in range(len(researcher_info)):
                for j in range(i+1,len(researcher_info)):
                    # src = researcher_info[i][2]
                    # dst = researcher_info[j][2]
                    src_first,src_last,src_id = researcher_info[i]
                    dst_first,dst_last,dst_id = researcher_info[j]

                    if src_id!=dst_id and src_id is not None and dst_id is not None:
                        researcher_edgelist[(src_id,dst_id)] += amount
                        researcher_edgelist[(dst_id,src_id)] += amount

                        #add researcher names to dictionary
                        new_name = str(src_first).strip(" ") + "_" + str(src_last).strip(" ")
                        researchers[src_id].add(new_name.lower())
                        
                        new_name = str(dst_first).strip(" ") + "_" + str(dst_last).strip(" ")
                        researchers[dst_id].add(new_name.lower())
        
        elif len(researcher_info)==1: #add self loops for single researcher awards to make it easier to check for correctness
            first,last,id = researcher_info[0]
            if id is not None:
                researcher_edgelist[(id,id)] += amount
                new_name = str(first).strip(" ") + "_" + str(last).strip(" ")
                researchers[id].add(new_name.lower())

#check for multiple names per researcher
c = 0
for researcher in researchers:
    if len(researchers[researcher])>1:
        c+=1    
print("number of researchers with multiple names: ", c)

#taking a look at the bad data
for researcher in researchers:
    if len(researchers[researcher])>1:
        print(researchers[researcher])    

#drop bad data
researcher_edgelist = {k:v for k,v in researcher_edgelist.items() if len(researchers[k[0]])==1 and len(researchers[k[1]])==1}
researchers = {k:v for k,v in researchers.items() if len(v)==1}
        
print("number of edges in researcher edgelist: ", len(researcher_edgelist))
print("number of researchers: ", len(researchers))

nodemap = {}
for i, researcher in enumerate(researchers):
    nodemap[researcher] = i

#write smat file
with open(os.path.join(output_dir,'nsf-coaward.smat'),'w') as fptr:
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(len(researchers),len(researchers),len(researcher_edgelist)))
    for (src,dst) in researcher_edgelist.keys():
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(nodemap[src],nodemap[dst],researcher_edgelist[(src,dst)]))

#write researcher names
with open(os.path.join(output_dir,'researcher_names.txt'),'w',encoding='utf-8') as fptr:
    for researcher in researchers:
        fptr.write('{0:d}\t{1:s}\t{2:s}\n'.format(nodemap[researcher],list(researchers[researcher])[0],researcher))



        