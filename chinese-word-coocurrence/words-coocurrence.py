import scipy.sparse as sp
import pandas as pd
import jieba
import os

# list all punctuations and filter them out
puncs = "()―《！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."

words_coocurrance = {}
words_counts = {}
root_dir = "Fudan/train/"
total_sentences = 0
# the dataset has articles in many topics, here we only choose "Politics"
for subfolder in ["C38-Politics"]:
    if subfolder[0] == ".":
        continue
    mydir = "Fudan/train/"+subfolder+"/utf8/"
    for filename in os.listdir(mydir):
        rptr = open(mydir+filename,"r")
        lines = rptr.readlines()
        text = "".join(l for l in lines if l[0] != '【')
        sentences = text.replace("\n","").replace(" ","").split("。")
        total_sentences += len(sentences)
        rptr.close()
        for sentence in sentences:
            seg_list = list(set([word for word in jieba.cut(sentence, cut_all=False) if word not in puncs and word.isdigit() == False]))
            for i in range(len(seg_list)):
                if seg_list[i] not in words_coocurrance:
                    words_coocurrance[seg_list[i]] = {}
                if seg_list[i] not in words_counts:
                    words_counts[seg_list[i]] = 1
                else:
                    words_counts[seg_list[i]] += 1
                tmp = words_coocurrance[seg_list[i]]
                for j in range(i+1,len(seg_list)):
                    if seg_list[j] not in tmp:
                        tmp[seg_list[j]] = 1
                    else:
                        tmp[seg_list[j]] += 1

wptr = open("words_coocurrence.labels","w")
words_map = {}
idx = 0
for word in words_counts.keys():
    words_map[word] = idx
    wptr.write(word+"\n")
    idx += 1
wptr.close()

import numpy as np
ei,ej,e = [],[],[]
for i,word1 in enumerate(words_coocurrance.keys()):
    tmp = words_coocurrance[word1]
    counts1 = words_counts[word1]
    idx1 = words_map[word1]
    for word2 in tmp.keys():
        w = max(0,np.log((tmp[word2]*total_sentences)/(counts1*words_counts[word2])))
        if w > 0:
            ei.append(idx1)
            ej.append(words_map[word2])
            e.append(w)

# make sure the graph is undirected
G = sp.csr_matrix((e,(ei,ej)),shape=(len(words_counts),len(words_counts)))
sel = G.T > G
G = G - G.multiply(sel) + G.T.multiply(sel)

ei = G.tocoo().row
ej = G.tocoo().col
e = G.tocoo().data

wptr = open("words_coocurrence.smat","w")
wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(len(words_counts),len(words_counts),len(ei)))
for i in range(len(ei)):
    wptr.write("{0:d}\t{1:d}\t{2:f}\n".format(ei[i],ej[i],e[i]))
wptr.close()