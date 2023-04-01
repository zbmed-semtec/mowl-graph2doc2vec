"""
    Created on Mar 2 9:30:27 2023

    @author: mariacastillo, bit2424
    
    This script contains the first version of the embedding aggregation techniques and evaluation.  

"""
from scipy.stats import pearsonr
from scipy import spatial
import json
import numpy as np
import pickle
import pandas as pd

def generate_URL(ident,array_object):
    # Generate a dictionary with URL to mach the respective embeddings 
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

def generate_emb(dict_url,embeddings_mesh):
    dict_emb={}
    for abstract_id in dict_url:
        URL_set = dict_url[abstract_id]
        for url in URL_set:
            if url in embeddings_mesh.keys():
                emb=embeddings_mesh[url]
                if abstract_id not in dict_emb.keys():
                    dict_emb[abstract_id]=[emb]
                else:
                    dict_emb[abstract_id].append(emb)
    return dict_emb  
    

def main():

    # Load embedings from mesh graph 
    with open('./Data/Output/2/Embeddings_mesh.pkl', 'rb') as file:
        embeddings_mesh = pickle.load(file)

    # Load the unique term graph 
    f=open('./Data/Output/3/Abstract2Graph_uniqueTerms.json')
    array_object = json.load(f)
    array_object={k: v for k, v in array_object.items() if v}     

    dict_url = generate_URL("MeSH",array_object)
    dict_emb = generate_emb(dict_url,embeddings_mesh)
    
    # Calculate average embedding from each abstract MeSH list 
    average_abs={}
    for k in dict_emb:
        a = np.array(dict_emb[k])
        av = np.mean(a, axis = 0)
        average_abs[k] = av.tolist()
    
    with open("./Data/Output/6/Graph2Vec_uniqueTerms.json", "w") as fp:
            json.dump(average_abs,fp,indent = 2) 
    
    
    # Load the enriched term graph 
    f=open('./Data/Output/4/Enriched_Graphs_v4.json')
    abs2grap_CC = json.load(f)
    abs2grap_CC={k: v for k, v in abs2grap_CC.items() if v}

    #Calculate avrg embeddings from each graph
    dic1 = {}
    url1 = 'http://purl.bioontology.org/ontology/MESH/'
    for i in abs2grap_CC.keys():
        for j in abs2grap_CC[i]:
            for k in j:
                if i in dic1.keys():
                    dic1[i].append(url1+k)
                else:
                    dic1[i]=[url1+k]


    dict_emb1 = generate_emb(dic1,embeddings_mesh)

    average_abs1 = {}
    
    for k in dict_emb1:
        a = np.array(dict_emb1[k])
        av = np.mean(a, axis = 0)
        average_abs1[k]= av.tolist()
    
    with open("./Data/Output/6/Graph2Vec_enrichedGraph.json", "w") as fp:
            json.dump(average_abs1,fp,indent = 2) 
    

main()