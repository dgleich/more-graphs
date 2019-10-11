#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : Oct. 11, 2019 10:37 AM
# @Author   : Veritas YIN
# @FileName : Graph_Gen.py
# @Version  : 1.2
# @IDE      : PyCharm
# @Github   : https://github.com/VeritasYin/Nx_Graph

import pandas as pd
import networkx as nx
from itertools import combinations
from pathlib import Path, PosixPath, PurePosixPath

# Data source: https://datasets.imdbws.com/
# Documentation for these data files can be found on http://www.imdb.com/interfaces/

# file path
data_path = PosixPath('~/Workspace/Data/IMDb/')
save_path = Path('./data')
crew_path = data_path / 'title.crew.tsv'
name_path = data_path / 'name.basics.tsv'

# load data
crew = pd.read_csv(crew_path, sep='\t', usecols=['tconst', 'directors', 'writers'])
name = pd.read_csv(name_path, sep='\t', index_col=['nconst'], usecols=['nconst', 'primaryName'], dtype=str)

# there are some duplicated items in the db, which need to be replaced.
alias = {'nm9014890': 'nm0232504',
         'nm9326757': 'nm7646438',
         'nm4906291': 'nm2416303',
         'nm10576972': 'nm10576752',
         'nm9786401': 'nm9741284',
         'nm9450471': 'nm3188149',
         'nm6706642': 'nm6698389',
         'nm8357745': 'nm4126155',
         'nm9407920': 'nm7140450',
         'nm6522433': 'nm0674902',
         'nm8911512': 'nm0025825',
         'nm1631626': 'nm1190154',
         'nm10892213': 'nm7208188',
         'nm9442622': 'nm8635223',
         'nm9492632': 'nm7155930',
         'nm8348107': 'nm5142065',
         'nm9832657': 'nm9832450',
         'nm7848976': 'nm5637661',
         'nm9400577': 'nm0612786'}


def build_graph(x, y, dic):
    # build a graph by networkx
    g = nx.Graph()

    for item, id in zip(x, y):
        # get the list of directors for each entity
        item_list = item.split(',')
        item_rep = [dic[x] if x in dic else x for x in item_list]

        if len(item_list) > 1:
            # create the combinations between item who share the same tid
            for node in list(combinations(item_rep, 2)):
                # check whether the edge exists
                # assign or append $tid to the attribute 'link' of the edge
                if g.has_edge(node[0], node[1]):
                    g[node[0]][node[1]]['link'].append(id)
                else:
                    g.add_edge(node[0], node[1], link=[id])
        else:
            # add a node (not \N) to the graph
            if item != '\\N':
                node = alias[item] if item in alias else item
                g.add_node(node)

    return g


def graph_filter(g, thrd=1):
    # filter the nodes whose linkage >= $thrd
    # attribute 'weight' = num of node linkage
    w_edges = ((u, v, {'weight': len(d)})
               for (u, v, d) in g.edges(data='link') if len(d) >= thrd)

    # build a new graph, each node of which has at least $thrd edge
    gw = nx.Graph()
    gw.update(w_edges)

    return gw


def graph_save(g, label, path, dtype, ftype='smat'):
    if not path.exists():
        path.mkdir()

    n_node = g.number_of_nodes()
    n_edge = g.number_of_edges()
    # print(n_node, n_edge)

    # hash nodes to index in 'node_hash' and record the mapping in 're_hash'
    node_hash = pd.Series(index=g.nodes, data=range(n_node))

    # it is not safe to using the following code to construct the hashing dict
    # real_value = [label[x] for x in node_hash.index]

    # it is recommended to use 'try - expect' to construct the hash mapping
    real_value = []
    for x in node_hash.index:
        try:
            real_value.append(label[x])
        except:
            real_value.append(x)
            print(f'WARNING: {dtype} key {x} is missing!')

    # keep a copy of original mapping
    re_hash = pd.DataFrame(index=node_hash.values, data=real_value)

    lpath = path / f'IMDb_{dtype}.labels'
    # write labels to file
    re_hash.to_csv(lpath, index=False, header=False)
    # if the double quote need be removed, use the following code:
    # import csv
    # re_hash.to_csv(file_path, header=False, index= False, sep=' ',
    #                quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")

    # write the graph to smat file
    spath = lpath.with_suffix(f'.{ftype}')
    with open(spath, 'w') as f:
        print(f'{n_node}\t{n_node}\t{n_edge}', file=f)
        for (u, v, d) in g.edges(data='weight'):
            u = node_hash[u]
            v = node_hash[v]
            print(f'{u}\t{v}\t{d}', file=f)
            print(f'{v}\t{u}\t{d}', file=f)
    print(f'The {dtype} graph has been written to {spath} with {n_node} nodes and {n_edge} edges.')


if __name__ == "__main__":
    # director graph
    g_directors = build_graph(crew.directors, crew.tconst, alias)
    gw_directors = graph_filter(g_directors)
    graph_save(gw_directors, name.primaryName, save_path, 'directors')

    # writer graph
    g_writers = build_graph(crew.writers, crew.tconst, alias)
    gw_writers = graph_filter(g_writers)
    graph_save(gw_writers, name.primaryName, save_path, 'writers')
