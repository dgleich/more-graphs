from neo4j import GraphDatabase
import pandas as pd
import scipy.sparse as sp
import numpy as np

# Connect to the reactome database. 
# You might need to replace the "login_id", "login_token" with yours.
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("login_id", "login_token"))

# Nodes with the following types are considered as basic nodes (i.e. they cannot be broken down).
basic_elements = set(["ChemicalDrug","ProteinDrug","EntityWithAccessionedSequence",
    "Polymer","SimpleEntity","GenomeEncodedEntity"])

# This functions will extract all reactions from the reatome dataset related to human immune system
def extract_immune_reactions(tx):
    reaction_ids = []
    for record in tx.run("MATCH (p:Pathway{stId:\"R-HSA-168256\"})-[:hasEvent*]->(rle:ReactionLikeEvent)"
                        "RETURN rle.stId as Reaction"):
        reaction_ids.append(record["Reaction"])
    return list(set(reaction_ids))

# This function will extract all participants (inputs, outputs, catalysts) from reactions.
# Complex nodes will be broken down recursively into basic nodes as defined by "basic_elements".
def get_elements(tx,stIds):
    element_ids = set()
    for i,stId in enumerate(stIds):
        print(i,len(stIds))
        stk = []
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:input|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:output|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:catalystActivity|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
        while len(stk) > 0:
            tmp = stk.pop()
            id = tmp[0]
            Class = tmp[1]
            if Class in basic_elements:
                element_ids.add(id)
            else:
                for member in tx.run("MATCH (r:PhysicalEntity{stId:{Participant}})-[:hasComponent|hasMember|hasCandidate*]->(mem:PhysicalEntity)"
                                     "RETURN mem.stId as Member, mem.schemaClass as Class",Participant=id):
                    stk.append((member["Member"],member["Class"]))
                element_ids.add(id)
    return element_ids

with driver.session() as session:
    reaction_ids = session.read_transaction(extract_immune_reactions)
    element_ids = session.read_transaction(get_elements,reaction_ids)

# This function will map the reactome id of each element into an external database id. 
# Each entry in the mapping will look like: stId -> (ref_id, database_name)
# Multiple entries can be mapped to the same external database id.
# Elements that cannot be found in external database will have the same "ref_id" as "stId" and "Unknown" for "database_name"
def stId_to_ref(tx,stIds):
    stId_to_ref_map = {}
    for stId in stIds:
        for record in tx.run("MATCH (r:PhysicalEntity{stId:{stId}})-[:referenceEntity]->(re:ReferenceEntity)"
                             "RETURN re.identifier AS ref_id, re.databaseName AS database_name",stId=stId):
            stId_to_ref_map[stId] = (record["ref_id"],record["database_name"])
        if stId not in stId_to_ref_map:
            stId_to_ref_map[stId] = (stId,"Unknown")
    return stId_to_ref_map

with driver.session() as session:
    stId_to_ref_map = session.read_transaction(stId_to_ref,list(element_ids))

# Identify all unique external database ids.
unique_refs = set([val[0] for val in stId_to_ref_map.values()])
unique_refs_to_dataset = {val[0]:val[1] for val in stId_to_ref_map.values()}

# Adding any new elements in the interaction network that don't participate any pathways.
interaction_df = pd.read_table("reactome.homo_sapiens.interactions.tab-delimited.txt")
for i in range(interaction_df.shape[0]):
    curr_row = interaction_df.iloc[i]
    uniprotkb1 = curr_row["# Interactor 1 uniprot id"].split(":")[-1]
    uniprotkb2 = curr_row["Interactor 2 uniprot id"].split(":")[-1]
    ensemble1 = curr_row["Interactor 1 Ensembl gene id"].split(":")[-1]
    ensemble2 = curr_row["Interactor 2 Ensembl gene id"].split(":")[-1]
    if uniprotkb1 not in unique_refs and ensemble1 not in unique_refs:
        unique_refs.add(uniprotkb1)
        unique_refs_to_dataset[uniprotkb1] = "UniProt"
    if uniprotkb2 not in unique_refs and ensemble2 not in unique_refs:
        unique_refs.add(uniprotkb2)
        unique_refs_to_dataset[uniprotkb2] = "UniProt"

# Build a unified index on all elements and also add nodes for each reaction.
unique_refs = sorted(list(unique_refs))
unique_ids_index = {unique_refs[i]:i for i in range(len(unique_refs))}
counts = len(unique_ids_index)
for action_id in sorted(reaction_ids):
    unique_ids_index[action_id] = counts
    counts += 1

# This function will add unidirectional edges for "input -> reaction" and "reaction -> output", 
# as well as bidirectional edges for "catalyst -- reaction".
def build_network(tx, stIds, unique_ids_index):
    ei,ej = [],[]
    counts = len(unique_ids_index)
    for i,stId in enumerate(stIds):
        print(i,len(stIds))
        stk = []
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:input|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
            if record["Participant"] in stId_to_ref_map:
                ei.append(unique_ids_index[stId_to_ref_map[record["Participant"]][0]])
            else:
                ei.append(unique_ids_index[record["Participant"]])
            ej.append(unique_ids_index[stId])
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:output|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
            if record["Participant"] in stId_to_ref_map:
                ej.append(unique_ids_index[stId_to_ref_map[record["Participant"]][0]])
            else:
                ej.append(unique_ids_index[record["Participant"]])
            ei.append(unique_ids_index[stId])
        for record in tx.run("MATCH (r:ReactionLikeEvent{stId:{stId}})-[:catalystActivity|physicalEntity*]->(pe:PhysicalEntity)"
                             "RETURN DISTINCT pe.stId as Participant, pe.schemaClass as Class",stId=stId):
            stk.append((record["Participant"],record["Class"]))
            if record["Participant"] in stId_to_ref_map:
                ei.append(unique_ids_index[stId_to_ref_map[record["Participant"]][0]])
            else:
                ei.append(unique_ids_index[record["Participant"]])
            ej.append(unique_ids_index[stId])
            if record["Participant"] in stId_to_ref_map:
                ej.append(unique_ids_index[stId_to_ref_map[record["Participant"]][0]])
            else:
                ej.append(unique_ids_index[record["Participant"]])
            ei.append(unique_ids_index[stId])
        while len(stk) > 0:
            tmp = stk.pop()
            id = tmp[0]
            Class = tmp[1]
            if id in stId_to_ref_map:
                src = unique_ids_index[stId_to_ref_map[id][0]]
            else:
                src = unique_ids_index[id]
            if Class not in basic_elements:
                tmps = []
                for member in tx.run("MATCH (r:PhysicalEntity{stId:{Participant}})-[:hasComponent|hasMember|hasCandidate*]->(mem:PhysicalEntity)"
                                     "RETURN mem.stId as Member, mem.schemaClass as Class",Participant=id):
                    stk.append((member["Member"],member["Class"]))
                    tmps.append((member["Member"],member["Class"]))
                if len(tmps) > 0:
                    for tmp in tmps:
                        if tmp[0] in stId_to_ref_map:
                            dst = unique_ids_index[stId_to_ref_map[tmp[0]][0]]
                        else:
                            dst = unique_ids_index[tmp[0]]
                        ei.append(src)
                        ej.append(dst)
                        ej.append(src)
                        ei.append(dst)
    return ei,ej

with driver.session() as session:
    ei,ej = session.read_transaction(build_network,reaction_ids,unique_ids_index)

# Combining the pathway network and the interaction network. 
# Edges in the interaction network are considered as bidirectional.
for i in range(interaction_df.shape[0]):
    curr_row = interaction_df.iloc[i]
    uniprotkb1 = curr_row["# Interactor 1 uniprot id"].split(":")[-1]
    uniprotkb2 = curr_row["Interactor 2 uniprot id"].split(":")[-1]
    ensemble1 = curr_row["Interactor 1 Ensembl gene id"].split(":")[-1]
    ensemble2 = curr_row["Interactor 2 Ensembl gene id"].split(":")[-1]
    if uniprotkb1 in unique_ids_index:
        src = unique_ids_index[uniprotkb1]
    else:
        src = unique_ids_index[ensemble1]
    if uniprotkb2 in unique_ids_index:
        dst = unique_ids_index[uniprotkb2]
    else:
        dst = unique_ids_index[ensemble2]
    ei.append(src)
    ej.append(dst)
    ei.append(dst)
    ej.append(src)

G = sp.csr_matrix((np.ones(len(ei)),(ei,ej)),shape=(len(unique_ids_index),len(unique_ids_index)))
G = (G>0).astype(np.int64)
ei = G.tocoo().row
ej = G.tocoo().col
e = G.tocoo().data

wptr = open("reactome-pathway.smat","w")
wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(len(unique_ids_index),len(unique_ids_index),len(ei)))
for i in range(len(ei)):
    wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(ei[i],ej[i],e[i]))

wptr.close()

wptr = open("reactome-pathway.labels","w")
for ref in unique_refs:
    dataset = unique_refs_to_dataset[ref]
    if dataset == "Unknown":
        dataset = "Reactome"
    wptr.write(ref+", "+dataset+", element"+"\n");

for action_id in sorted(reaction_ids):
    wptr.write(action_id+", Reactome"+", reaction"+"\n")

wptr.close()