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

def add_cos_similarity(relish_pairs, avrg_graph_emb,name):
    result_list_mesh = calculate_cos(relish_pairs,avrg_graph_emb)
    result_list_mesh = np.arccos(result_list_mesh) / np.pi
    relish_pairs[name] = result_list_mesh

def main():

    relish_pairs = pd.read_csv('./Data/Input/7/relish_existing_pairs.tsv', sep='\t')
    
    #Load the vectors representing the documents with the unique term graphs
    with open('./Data/Output/6/Graph2Vec_uniqueTerms.json') as f:
        avrg_abs_unique_mesh_graph= json.load(f)

    add_cos_similarity(relish_pairs, avrg_abs_unique_mesh_graph,'Cos Sim unique')
    
    #Load the vectors representing the documents with the enriched graphs unique
    with open('./Data/Output/6/Graph2Vec_enrichedGraph.json') as f:
        avrg_abs_enriched_mesh_graph = json.load(f)
             
    add_cos_similarity(relish_pairs, avrg_abs_enriched_mesh_graph,'Cos Sim enriched')
    
    #Load baseline
    baseline_cosine_sim = pd.read_csv('./Data/Input/7/whatizit_exisiting_cosine_relish.tsv', sep='\t')
    results_baseline = np.array(baseline_cosine_sim['Cosine Similarity'])
    relish_pairs['Cos Sim Baseline'] = results_baseline
    
    relish_pairs.to_csv("./Data/Output/7/relish_pairs_cosine_similarity_v1.tsv",sep="\t")
    print(relish_pairs.head())
    
    #Correlation analysis
    
    
    relish_pairs['Cos Sim unique'][np.isnan(relish_pairs['Cos Sim unique'])] = 0
    relish_pairs['Cos Sim enriched'][np.isnan(relish_pairs['Cos Sim enriched'])] = 0
    results_baseline[np.isnan(results_baseline)] = 0
    corr1, _ = pearsonr(relish_pairs['Cos Sim unique'], relish_pairs['Cos Sim enriched'])
    corr2, _ = pearsonr(relish_pairs['Cos Sim unique'], results_baseline)
    corr3, _ = pearsonr(relish_pairs['Cos Sim enriched'], results_baseline)
    print(corr1,corr2,corr3)

main()