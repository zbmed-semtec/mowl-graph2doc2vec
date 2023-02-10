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

def add_edge(adj, src, dest):
    adj[src].append(dest) 
    adj[dest].append(src) 

def getIdx(id):
    if(id in id2idx):
        return id2idx[id]
    else:
        global idx_ref
        idx_ref+=1
        id2idx[id] = idx_ref
        id2idx[idx_ref] = id
        
        return idx_ref

def format_Big_2(raw_graph):
    v = len(raw_graph)

    new_G = [[] for i in range(v)]

    for edge in raw_graph:
        src = edge.src.split("/")[-1]
        rel = edge.rel.split("/")[-1]
        dst = edge.dst.split("/")[-1]
        add_edge(new_G,getIdx(src),getIdx(dst))

    return new_G

def format_Big(raw_graph):
    v = 0

    for section in raw_graph:
        v+=len(section)

    new_G = [[] for i in range(v)]

    for section in raw_graph:
        for edge in section:
            # print(edge.src)
            src = edge.src.split("/")[-1]
            rel = edge.rel.split("/")[-1]
            dst = edge.dst.split("/")[-1]
            add_edge(new_G,getIdx(src),getIdx(dst))

    return new_G

def format_Small(raw_graph):
    graphs = {}
    lost = set()
    for k,g in raw_graph.items():
        temp_G = []
        for edge,v in g.items():
            e1 = edge.split(" ")[0][4:len(edge.split(" ")[0])]
            e2 = edge.split(" ")[1][4:len(edge.split(" ")[1])]
            if(e1 in id2idx and e2 in id2idx):
                temp_G.append([id2idx[e1],id2idx[e2]])
            else:
                if(e1 not in id2idx): lost.add(e1)
                if(e2 not in id2idx): lost.add(e2)
                
        graphs[k] = temp_G
    
    print(lost)
    print(len(lost))
    return graphs


def main():
    with open('../../Data/Output/Abstract2Graph_Co_Occurrence_no_text_links.json') as f:
        Abstract_Graph_raw = json.load(f)
    
    Onto_graph_raw = []
    
    # with open('../../Data/Input/Graph_mesh_OWL2VEC.pkl', 'rb') as f:
    #     Onto_graph_raw = pickle.load(f)

    with (open("../../Data/Input/Graph_mesh_OWL2VEC.pkl", "rb")) as openfile:
        while True:
            try:
                Onto_graph_raw.append(pickle.load(openfile))
            except EOFError:
                break

    # print(Onto_graph_raw)
    
    #checkTypeofRelations(Onto_graph_raw)
    
    #Is a DAG
    global big_G
    global small_Gs
    global enriched_Gs
    
    # big_G = format_Big(Onto_graph_raw)
    #The problem is not the reading.
    checkTypeofRelations(Onto_graph_raw)
    #big_G = format_Big(Onto_graph_raw)
    #small_Gs = format_Small(Abstract_Graph_raw)


main()