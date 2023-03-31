"""
    Created on Fri Feb 10 16:25:45 2023

    @author: mariacastillo

    This script contains the first version of the embedding aggregation techniques and evaluation.  
"""
from scipy import spatial
import json
import numpy as np
import pickle

# Load dictionaries of mesh terms
# Load embedings from mesh graph 
f=open('mesh_dict_after_match_PMID.json')

with open('Embedings_mesh.pkl', 'rb') as file:
    Embedings_mesh = pickle.load(file)

array_object = json.load(f)
array_object={k: v for k, v in array_object.items() if v}

def generate_URL(ident,array_object):
# Generate a dictionary with URL to mach the rrepective embdeingss 
    url1='http://purl.bioontology.org/ontology/MESH/'
    
    dict_url={}
    for i in array_object: #i is going to be PMID
        for j in array_object[i]:
            mesh_term=j.replace(ident, "")
            if i not in dict_url.keys():
                dict_url[i]=[url1+mesh_term] 
            else:
                dict_url[i].append((url1+mesh_term))
    return dict_url

def generate_emb(dict_url):
    dict_emb={}
    for n in dict_url:
        URL_set=dict_url[n]
        for m in URL_set:
            if m in Embedings_mesh.keys():
                emb=Embedings_mesh[m]
                if i not in dict_emb.keys():
                    dict_emb[n]=[emb]
                else:
                    dict_emb[n].append(emb)
    return dict_emb        

dict_url=generate_URL("MeSH",array_object)
dict_emb=generate_emb(dict_url)
# Calculate average embeding frrom each abstract 
average_abs={}
for k in dict_emb:
    a = np.array(dict_emb[k])
    av=np.mean(a, axis = 0)
    average_abs[k]=av   

"""
import json

# create json object from dictionary
json = json.dumps(average_abs)

# open file for writing, "w" 
f = open("Average_abstracts.json","w")

# write json object to file
f.write(json)

# close file
f.close()
"""

import pandas as pd
var = pd.read_csv('relish_existing_pairs.tsv', sep='\t')

def calculate_cos(var,average_abs):
    result=[]
    for g,h in zip(var.PMID1,var.PMID2):
        if str(g) in average_abs.keys() and str(h) in average_abs.keys():
            vec1=average_abs[str(g)]
            vec2=average_abs[str(h)]
            result.append(1 - spatial.distance.cosine(vec1, vec2))
        else:
            result.append(0)
    return result

result=calculate_cos(var,average_abs)
result = np.arccos(result) / np.pi
var['Cos Sim M1'] = result
print(var)

f=open('Enriched_Graphs_v3_nx.json')
abs2grap_CC = json.load(f)
abs2grap_CC={k: v for k, v in abs2grap_CC.items() if v}

dic1={}
url1='http://purl.bioontology.org/ontology/MESH/'
for i in abs2grap_CC.keys():

    for j in abs2grap_CC[i]:
        for k in j:
            if i in dic1.keys():
                dic1[i].append(url1+k)
            else:
                dic1[i]=[url1+k]


dict_emb1=generate_emb(dic1)

average_abs1={}
for k in dict_emb1:
    a = np.array(dict_emb1[k])
    av=np.mean(a, axis = 0)
    average_abs1[k]=av 
    
result2=calculate_cos(var,average_abs1)
result2 = np.arccos(result2) / np.pi

var['Cos Sim M2'] = result2
print(var)

var.to_csv('relish_existing_pairs_cosine_similarity.csv', sep='\t', index=False)

var2 = pd.read_csv('whatizit_exisiting_cosine_relish.tsv', sep='\t')

results3=np.array(var2['Cosine Similarity'])

from scipy.stats import pearsonr
result[np.isnan(result)] = 0
result2[np.isnan(result2)] = 0
results3[np.isnan(results3)] = 0
corr1, _ = pearsonr(result, result2)
corr2, _ = pearsonr(result, results3)
corr3, _ = pearsonr(result2, results3)