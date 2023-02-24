"""
Here we optimize the algorithm not taking into account repeated nodes.
"""

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
    
    for k in relations.items():
        print(k)

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

    for section in raw_graph:
        v+=len(section)

    new_G = [set() for i in range(v)]

    for section in raw_graph:
        for edge in section:
            # print(edge.src)
            src = edge.src.split("/")[-1]
            rel = edge.rel.split("/")[-1]
            dst = edge.dst.split("/")[-1]
            add_edge(new_G,getIdx(src),getIdx(dst))

    out_G = [[] for i in range(v)]
    
    for id in range(v):
        for elem in new_G[id]:
            out_G[id].append(elem)
    
    return out_G

def add_edge(adj, src, dest):
    adj[src].add(dest) 
    adj[dest].add(src) 


def BFS(adj, src, dest, v, pred, dist):

    queue = []

    visited = [False for i in range(v)]  
    
    for i in range(v):
        dist[i] = 100000000
        pred[i] = -1  
    
    visited[src] = True  
    dist[src] = 0  
    queue.append(src)  

    while (len(queue) != 0):
        u = queue[0]  
        queue.pop(0)
        for i in range(len(adj[u])):
        
            if (visited[adj[u][i]] == False):
                visited[adj[u][i]] = True  
                dist[adj[u][i]] = dist[u] + 1  
                pred[adj[u][i]] = u  
                queue.append(adj[u][i])  

                if (adj[u][i] == dest):
                    return True  

    return False  

def getShortestDistance(adj, s, dest, v):
    
    pred=[0 for i in range(v)]
    dist=[0 for i in range(v)]  

    if (BFS(adj, s, dest, v, pred, dist) == False):
        print("Given source and destination are not connected")

    # vector path stores the shortest path
    path = []
    crawl = dest  
    path.append(crawl)  
    
    while (pred[crawl] != -1):
        path.append(pred[crawl])  
        crawl = pred[crawl]  
    

    # distance from source is in distance array
    # print("Shortest path length is : " + str(dist[dest]), end = '')

    # # printing path from source to destination
    # print("\nPath is : : ")
    
    out_path = [] 
    
    for i in range(len(path)-1, -1, -1):
        out_path.append(path[i])
        #print(id2idx[path[i]], end=' ')
    
    return out_path
    

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
    new_node_list = set()
    
    #print(graph)
    
    for edge in graph:
        source = edge[0]
        dest = edge[1]
        list = getShortestDistance(big_G, source, dest, idx_ref+1)
        for node in list:
            new_node_list.add(node)
    
    return [id2idx[x] for x in new_node_list]
    

def main():
    with open('../../Data/Output/Abstract2Graph_Co_Occurrence_no_text_links.json') as f:
        Abstract_Graph_raw = json.load(f)
    
    # with open('../../Data/Input/Graph_mesh.pkl', 'rb') as f:
    #     Onto_graph_raw = pickle.load(f)

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
        if(i==100):break

    #print(enriched_Gs)
    print(avrg//len(enriched_Gs))
    
    with open("../../Data/Output/Enriched_Graphs_v2.json", "w") as fp:
        json.dump(enriched_Gs,fp,indent = 2) 
    

main()