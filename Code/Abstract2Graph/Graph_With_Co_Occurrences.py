"""
    The algorithm generates links between 2 MESH concepts in a paragraph.
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
unique_nodes = set()

"""

"Pub_med_id" : occurrence_graph

"""
all_occurrence_graphs = {}

def filterGraph():
    new_graph_sz = len(unique_nodes) + (15*len(unique_nodes))//100
    sorted_graph = {k: v for k, v in sorted(occurrence_graph.items(), key=lambda item: -item[1])}
    new_graph = {}
    #print("LOL: ", sorted_graph["MeSHD007484 MeSHD014186"])
    for k in sorted_graph:
       new_graph[k] = sorted_graph[k]
       new_graph_sz-=1
       if(new_graph_sz == 0): break; 

    return new_graph


def count(sentence):
    
    if(type(sentence)==str):
        meshInSentence = re.findall("MeSH[A-Z]+[0-9]+", sentence)
        #If the same concept appears 2 times does that imply the co occurrence should be higher?
        for i in range(len(meshInSentence)):
            for j in range(i+1,len(meshInSentence)):
                meshTerm1 = meshInSentence[i] 
                meshTerm2 = meshInSentence[j]

                unique_nodes.add(meshTerm1)
                unique_nodes.add(meshTerm2)
                #making sure no double counting occurs.
                if(meshTerm1>meshTerm2):
                    meshTerm2 = meshInSentence[i] 
                    meshTerm1 = meshInSentence[j] 
                
                if(meshTerm1 != meshTerm2):
                    key = meshTerm1 + " " + meshTerm2
                    if(key in occurrence_graph.keys()):
                        occurrence_graph[key] += 1
                    else:
                        occurrence_graph[key] = 1


def main():
    df = pd.read_table('../../Data/Input/RELISH_documents_20220628_ann.tsv')
    df.columns = ['PMID', 'title', 'abstract']
    avrg_nodes = 0
    num_art = 0
    for index, row in df.iterrows():
        occurrence_graph.clear()
        unique_nodes.clear()
        
        num_art+=1
        
        #print(row['title'])
        count(row['title'])
        if(type(row['abstract'])==str):
            for sentence in row['abstract'].split("."):
                count(sentence)
        
        avrg_nodes+=len(unique_nodes)


        filtered_occurrence_graph = filterGraph()
        all_occurrence_graphs[row['PMID']] = filtered_occurrence_graph

    print("Avrg_nodes per article",avrg_nodes//num_art)

    with open("../../Data/Output/Abstract2Graph_Co_Occurrence.json", "w") as fp:
        json.dump(all_occurrence_graphs,fp,indent = 2) 



main()