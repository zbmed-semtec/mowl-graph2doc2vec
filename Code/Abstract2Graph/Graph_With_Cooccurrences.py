"""
    The algorithm generates links between 2 MESH concepts in a paragraph.
    The links are based on how many times the 2 terms appear in a sentence. 
    Then an edge between the x% of the most coo occurrent pairs is made.
"""
import pandas as pd


df = pd.read_table('../../Data/RELISH_documents_20220628_ann.tsv')
print(df.head())