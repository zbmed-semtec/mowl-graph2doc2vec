"""
    Created on Fri Feb 11 18:25:45 2023

    @author: mariacastillo, bit2424

    This script is generates vector embeddings from the graph projection of the MeSH ontology.
"""

import torch as th

import mowl
import pickle
import os
mowl.init_jvm("4g")

from pykeen.models import TransE
from mowl.projection.edge import Edge
from mowl.kge import KGEModel

# Open a file and use dump()
with open('./Data/Output/1/Graph_mesh.pkl', 'rb') as file:
    # A new file will be created
    edges = pickle.load(file)
    
triples_factory = Edge.as_pykeen(edges, create_inverse_triples = True)

pk_model = TransE(triples_factory=triples_factory, embedding_dim = 50, random_seed=42)

model = KGEModel(triples_factory, pk_model, epochs = 10, batch_size = 32)
model.train()
ent_embs = model.class_embeddings_dict
rel_embs = model.object_property_embeddings_dict

print(ent_embs)
print(rel_embs)

with open('./Data/Output/2/Embeddings_mesh.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(ent_embs, file)