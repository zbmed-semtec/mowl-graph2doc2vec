"""
Created on Fri Feb 11 16:25:45 2023

@author: mariacastillo, bit2424

This script is generates a graph projection of the MeSH ontology.
"""

# import sys
# sys.path.append('../../')
import mowl
import pickle
import os
mowl.init_jvm("4g")
from mowl.datasets import PathDataset
from mowl.projection import DL2VecProjector
from mowl.projection import OWL2VecStarProjector

# Data: mesh ontologies from https://bioportal.bioontology.org/ontologies/MESH?p=summary
dataset = PathDataset('./Data/Input/1/MESH.ttl')

# Setting parameters of the OWL2VEC projector
projector = OWL2VecStarProjector(
             bidirectional_taxonomy=True,
             include_literals = False,
             only_taxonomy = True)

# Project the ontologies to a graph
edges = projector.project(dataset.ontology)

# Save the graph in a pickle variable
with open('./Data/Output/1/Graph_mesh_OWL2VEC.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(edges, file)

print(edges[0].astuple())



