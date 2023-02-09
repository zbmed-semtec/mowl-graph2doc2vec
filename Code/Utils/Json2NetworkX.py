import json
import networkx as nx

def main():
    G_json = {}
    with open('../../Data/Output/Abstract2Graph_Co_Occurrence_no_text_links.json') as f:
        G_json = json.load(f)
    G_nx = nx.empty_graph()
    print(G_nx)
    nx.write_gexf(G_nx, "example.gexf")

main()