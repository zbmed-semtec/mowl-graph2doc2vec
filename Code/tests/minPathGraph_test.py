import json
import pickle
import mowl
mowl.init_jvm("4g")


id2idx = {}
big_G = []
idx_ref = -1

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

	new_G = [[] for i in range(v)]

	for section in raw_graph:
		for edge in section:
			# print(edge.src)
			src = edge.src.split("/")[-1]
			rel = edge.rel.split("/")[-1]
			dst = edge.dst.split("/")[-1]
			if(rel == "subclassof"):
				add_edge(new_G,getIdx(src),getIdx(dst))

	return new_G

def add_edge(adj, src, dest):
	adj[src].append(dest) 
	adj[dest].append(src) 


def BFS(adj, src, dest, v, pred, dist):

	queue = []

	visited = [False for i in range(v)]  
	
	for i in range(v):
		dist[i] = 1000000
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
	
	# predecessor[i] array stores predecessor of
	# i and distance array stores distance of i
	# from s
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
	print("Shortest path length is : " + str(dist[dest]), end = '')

	# printing path from source to destination
	print("\nPath is : : ")
	
	for i in range(len(path)-1, -1, -1):
		print( id2idx[path[i]], end=' ')
		
# Driver program to test above functions
if __name__=='__main__':
	
	# no. of vertices
	Onto_graph_raw = []
	with (open("../../Data/Input/Graph_mesh.pkl", "rb")) as openfile:
		while True:
			try:
				Onto_graph_raw.append(pickle.load(openfile))
			except EOFError:
				break
	
	big_G = format_Big(Onto_graph_raw)
	
	source = 0
	dest = 7  
	print(id2idx[source])
	print(id2idx[dest])
	getShortestDistance(big_G, source, dest, len(big_G)+1)  
