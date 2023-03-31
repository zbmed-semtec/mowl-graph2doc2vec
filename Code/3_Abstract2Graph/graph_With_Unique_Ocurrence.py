"""
    @author: bit2424
    
    The algorithm generates a list with the unique MeSH identified in each document abstract.
"""
import pandas as pd
import re
import json


unique_nodes = {}

"""
"Pub_med_id" : unique_nodes_list
"""
graph = {}

def count(sentence):
    if(type(sentence)==str):
        meshInSentence = re.findall("MeSH[A-Z]+[0-9]+", sentence)
        for i in range(len(meshInSentence)):
            meshTerm1 = meshInSentence[i]
            if(meshTerm1 not in unique_nodes):
                unique_nodes[meshTerm1] = 1


def main():
    df = pd.read_table('./Data/Input/3/RELISH_documents_20220628_ann.tsv')
    df.columns = ['PMID', 'title', 'abstract']
    avrg_nodes = 0
    num_art = 0
    for index, row in df.iterrows():
        unique_nodes.clear()
        
        num_art+=1
        
        count(row['title'])
        if(type(row['abstract'])==str):
            for sentence in row['abstract'].split("."):
                count(sentence)
        
        avrg_nodes+=len(unique_nodes)

        graph[row['PMID']] = list(unique_nodes.keys())

    print("Avrg_nodes per article",avrg_nodes//num_art)

    with open("./Data/Output/3/Abstract2Graph_uniqueTerms.json", "w") as fp:
        json.dump(graph,fp,indent = 2) 



main()