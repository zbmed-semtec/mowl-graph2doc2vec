"""
    The algorithm generates a list with the unique MeSH identified in the abstract.
"""
import pandas as pd
import re
import json


unique_nodes = set()

"""
"Pub_med_id" : unique_nodes_list
"""
all_occurrence_graphs = {}

def count(sentence):
    
    if(type(sentence)==str):
        meshInSentence = re.findall("MeSH[A-Z]+[0-9]+", sentence)
        #If the same concept appears 2 times does that imply the co occurrence should be higher?
        for i in range(len(meshInSentence)):
            meshTerm1 = meshInSentence[i] 
            unique_nodes.add(meshTerm1)


def main():
    df = pd.read_table('./Data/Input/RELISH_documents_20220628_ann.tsv')
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

        all_occurrence_graphs[row['PMID']] = list(unique_nodes)

    print("Avrg_nodes per article",avrg_nodes//num_art)

    with open("./Data/Output/Abstract2Graph_uniqueTerms.json", "w") as fp:
        json.dump(all_occurrence_graphs,fp,indent = 2) 



main()