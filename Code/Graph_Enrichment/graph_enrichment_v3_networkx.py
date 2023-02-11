"""
Here we take into account the weighted nodes of the based on the amount of time they were visited.
Network_x library
"""
import timeit
import json
import pickle
import mowl
mowl.init_jvm("4g")
import networkx as nx

id2idx = {}
idx_ref = -1
big_G = nx.Graph()

small_Gs = {}

enriched_Gs = {}

augmented_Gs = []

def getIdx(id):
    if(id in id2idx):
        return id2idx[id]
    else:
        global idx_ref
        idx_ref+=1
        id2idx[id] = idx_ref
        id2idx[idx_ref] = id
        
        return idx_ref

def format_Big(raw_graph):
    v = 0
    new_G = nx.Graph()
    
    for section in raw_graph:
        for edge in section:
            # print(edge.src)
            src = edge.src.split("/")[-1]
            rel = edge.rel.split("/")[-1]
            dst = edge.dst.split("/")[-1]
            new_G.add_edge(getIdx(src),getIdx(dst))
    
    return new_G


def getShortestDistance(adj, s, dest, v):
    
        
    path = G = nx.shortest_path(adj,s,dest)
    
    #print(path)
    
    return path
    

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
    
    with open("../../Data/Output/Lost_terms.json", "w") as fp:
        json.dump([x for x in lost],fp,indent = 2)
    return graphs

def enrich_graph(graph):
    new_nodes = {}
    
    for edge in graph:
        source = edge[0]
        dest = edge[1]
        list = getShortestDistance(big_G, source, dest, idx_ref+1)
        for node in list:
            if(node in new_nodes):
                new_nodes[node] += 1
            else:
                new_nodes[node] = 1
    
    return [{id2idx[k]:v} for k,v in new_nodes.items()]
    

def main():
    with open('../../Data/Output/Abstract2Graph_Co_Occurrence_no_text_links.json') as f:
        Abstract_Graph_raw = json.load(f)

    Onto_graph_raw = []
    with (open("../../Data/Input/Graph_mesh_OWL2VEC.pkl", "rb")) as openfile:
        while True:
            try:
                Onto_graph_raw.append(pickle.load(openfile))
            except EOFError:
                break

    
    #checkTypeofRelations(Onto_graph_raw)
    
    #Is a DAG
    global big_G
    global small_Gs
    global enriched_Gs
    
    big_G = format_Big(Onto_graph_raw)
    small_Gs = format_Small(Abstract_Graph_raw)
    avrg = 0
    
    i = 0
    
    for k in small_Gs:
        enriched_Gs[k] = enrich_graph(small_Gs[k])
        if("owl#Thing" in enriched_Gs[k]): enriched_Gs[k].remove("owl#Thing")
        avrg += len(enriched_Gs[k])
        i+=1
        if(i==10):break

    #print(avrg//len(enriched_Gs))
    
    with open("../../Data/Output/Enriched_Graphs_v3_nx.json", "w") as fp:
        json.dump(enriched_Gs,fp,indent = 2) 


#Execution time 33 seconds
t_0 = timeit.default_timer()
main()
t_1 = timeit.default_timer()
elapsed_time = round((t_1 - t_0), 3)
print(f"Elapsed time: {elapsed_time}")