import sys
sys.path.append('../../')
import mowl
import pickle
import os
mowl.init_jvm("4g")
from mowl.datasets import PathDataset
from mowl.projection import DL2VecProjector
from mowl.projection import OWL2VecStarProjector

# Data: mesh ontologies from https://bioportal.bioontology.org/ontologies/MESH?p=summary
dataset = PathDataset('Data/Input/MESH.ttl')

# Setting parameters of the OWL2VEC projector
projector = OWL2VecStarProjector(
             bidirectional_taxonomy=True,
             include_literals = False,
             only_taxonomy = True)

# Project the ontologies to a graph
edges = projector.project(dataset.ontology)

# Save the graph in a pickle variable
with open('Graph_mesh.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(edges, file)

assert os.path.exists('Graph_mesh.pkl') 

print(edges[0].astuple())



