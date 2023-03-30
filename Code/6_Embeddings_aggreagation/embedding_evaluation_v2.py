#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 2 9:30:27 2023

@author: mariacastillo, bit2424
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

def calculate_cos(relish_pairs,average_abs):
    result=[]
    for g,h in zip(relish_pairs.PMID1,relish_pairs.PMID2):
        if str(g) in average_abs.keys() and str(h) in average_abs.keys():
            vec1=average_abs[str(g)]
            vec2=average_abs[str(h)]
            result.append(1 - spatial.distance.cosine(vec1, vec2))
        else:
            result.append(0)
    return result

def main():

    # Load embedings from mesh graph 
    with open('./Data/Input/Embedings_mesh.pkl', 'rb') as file:
        embeddings_mesh = pickle.load(file)

    # Load dictionaries of mesh terms
    f=open('./Data/Output/Abstract2Graph_uniqueTerms.json')
    array_object = json.load(f)
    array_object={k: v for k, v in array_object.items() if v}     

    dict_url=generate_URL("MeSH",array_object)
    dict_emb=generate_emb(dict_url,embeddings_mesh)
    
    # Calculate average embedding from each abstract MeSH list 
    average_abs={}
    for k in dict_emb:
        a = np.array(dict_emb[k])
        av = np.mean(a, axis = 0)
        average_abs[k] = av
    
    relish_pairs = pd.read_csv('./Data/Input/relish_existing_pairs.tsv', sep='\t')

    result_list_mesh = calculate_cos(relish_pairs,average_abs)
    result_list_mesh = np.arccos(result_list_mesh) / np.pi
    relish_pairs['Cos Sim M1'] = result_list_mesh
    print(relish_pairs)

    #Calculate avrg embeddings from each abstract MeSH graph
    f=open('./Data/Output/Enriched_Graphs_v4.json')
    abs2grap_CC = json.load(f)
    abs2grap_CC={k: v for k, v in abs2grap_CC.items() if v}

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
        average_abs1[k]=av 
        
    result_graph_mesh = calculate_cos(relish_pairs,average_abs1)
    result_graph_mesh = np.arccos(result_graph_mesh) / np.pi

    relish_pairs['Cos Sim M2'] = result_graph_mesh
    
    baseline_cosine_sim = pd.read_csv('./Data/Input/whatizit_exisiting_cosine_relish.tsv', sep='\t')

    results_baseline = np.array(baseline_cosine_sim['Cosine Similarity'])
    
    relish_pairs['Cos Sim Baseline'] = results_baseline
    
    relish_pairs.to_csv("./Data/Output/relish_pairs_cosine_similarity.tsv",sep="\t")
    print(relish_pairs.head())
    
    #Correlation analysis
    result_list_mesh[np.isnan(result_list_mesh)] = 0
    result_graph_mesh[np.isnan(result_graph_mesh)] = 0
    results_baseline[np.isnan(results_baseline)] = 0
    corr1, _ = pearsonr(result_list_mesh, result_graph_mesh)
    corr2, _ = pearsonr(result_list_mesh, results_baseline)
    corr3, _ = pearsonr(result_graph_mesh, results_baseline)
    print(corr1,corr2,corr3)

main()