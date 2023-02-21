import json
import pickle
import mowl
mowl.init_jvm("4g")

id2idx = {}
idx_ref = -1
big_G = []

small_Gs = {}

enriched_Gs = {}

augmented_Gs = []

def checkTypeofRelations(graph):
    relations = {}
    for section in graph:
        for edge in section:
            rel = edge.rel.split("/")[-1]
            if(rel not in relations.keys()):
                relations[rel] = 1
            else:
                relations[rel] += 1
    sum = 0
    for k,v in relations.items():
        sum+= v
        print(k,v)
    print(sum)


def main():
    with open('./Data/Output/Abstract2Graph_Co_Occurrence.json') as f:
        Abstract_Graph_raw = json.load(f)
    
    Onto_graph_raw = []
    
    with (open("./Data/Input/Graph_mesh_OWL2VEC.pkl", "rb")) as openfile:
        while True:
            try:
                Onto_graph_raw.append(pickle.load(openfile))
            except EOFError:
                break
    
    #Is a DAG
    global big_G
    global small_Gs
    global enriched_Gs
    
    checkTypeofRelations(Onto_graph_raw)


main()