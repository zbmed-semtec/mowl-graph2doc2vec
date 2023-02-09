import json
import pickle
import mowl
mowl.init_jvm("4g")

big_G = {}
small_Gs = []

def checkTypeofRelations(graph):
    relations = {}
    for section in graph:
        for edge in section:
            rel = edge.rel.split("/")[-1]
            if(rel not in relations.keys()):
                relations[rel] = 1
            else:
                relations[rel] += 1
    
    for k in relations.items():
        print(k)

def goUpGraph(graph):
    visited = [] 



def format_Big(raw_graph):
    new_G = {}
    
    for section in raw_graph:
        for edge in section:
            src = edge.src.split("/")[-1]
            new_G[src] = list()
    
    for section in raw_graph:
        for edge in section:
            # print(edge.src)
            src = edge.src.split("/")[-1]
            rel = edge.rel.split("/")[-1]
            dst = edge.dst.split("/")[-1]
            if(rel == "subclassof"):
               new_G[src].append(dst)

    return new_G

def format_Small(raw_graph):

    return []

def main():
    with open('../../Data/Output/Abstract2Graph_Co_Occurrence_no_text_links.json') as f:
        Abstract_Graph_raw = json.load(f)
    
    # with open('../../Data/Input/Graph_mesh.pkl', 'rb') as f:
    #     Onto_graph_raw = pickle.load(f)

    Onto_graph_raw = []
    with (open("../../Data/Input/Graph_mesh.pkl", "rb")) as openfile:
        while True:
            try:
                Onto_graph_raw.append(pickle.load(openfile))
            except EOFError:
                break

    
    checkTypeofRelations(Onto_graph_raw)
    # big_G is a tree
    big_G = format_Big(Onto_graph_raw)
    print("size big_G",len(big_G))

    sum = 0
    for k in big_G:
        sum+=len(big_G[k])

    print("sum big_G links",sum)
    format_Small(Abstract_Graph_raw)

main()