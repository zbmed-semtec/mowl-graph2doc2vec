"""
    @author: bit2424
    
    The script generates links between 2 MESH concepts in a paragraph.
    The links are based on how many times the 2 terms appear in a sentence. 
    Then an edge between the x% of the most co occurrent pairs is made.
"""
import pandas as pd
import re
import json

"""

"MeSH_id_1 MeSH_id_2" : #co-occurrences

"""
occurrence_graph = {}

"""

"Pub_med_id" : occurrence_graph

"""
all_occurrence_graphs = {}


def count(sentence):
    if(type(sentence)==str):
        meshInSentence = re.findall("MeSH[A-Z]+[0-9]+", sentence)
        for i in range(len(meshInSentence)):
            meshTerm1 = meshInSentence[i]
            if(meshTerm1 not in occurrence_graph):
                occurrence_graph[meshTerm1] = 1
            else:
                occurrence_graph[meshTerm1] += 1


def main():
    global occurrence_graph
    global all_occurrence_graphs
    
    df = pd.read_table('./Data/Input/3/RELISH_documents_20220628_ann.tsv')
    df.columns = ['PMID', 'title', 'abstract']
    num_art = 0
    for index, row in df.iterrows():
        occurrence_graph.clear()
        
        if(len(row['PMID'].split(" "))>2):
            continue    
        
        #print(row['title'])
        count(row['title'])
        if(type(row['abstract'])==str):
            for sentence in row['abstract'].split("."):
                count(sentence)
        
        
        all_occurrence_graphs[row['PMID']] = list(occurrence_graph.items())
        
    with open("./Data/Output/3/Abstract2Graph_Cnt_Occurrence.json", "w") as fp:
        json.dump(all_occurrence_graphs,fp,indent = 2) 



main()