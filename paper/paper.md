---
title: 'Using ontology-based graph embeddings as background knowledge for doc-2-doc similarity'
tags:
  - Graph embeddings
  - Document similarity
  - Ontology background knowledge
  - BioHackathon MENA
authors:
  - name: Nelson David Quiñones
    orcid: 0000-0002-5037-0443
    affiliation: 
    - 1
    - 2
  - name: Rahaf Alayed
    orcid: 0000-0002-7083-5893
    affiliation: 2
  - name: Layan Aljohani
    orcid: 0000-0001-6954-2973
    affiliation: 3
  - name: Asmaa Alqhtani
    orcid: 0000-0002-3119-5109
    affiliation: 4
  - name: Maria G Gomez Castillo
    orcid: 0000-0000-0000-0000
    affiliation: 5
  - name: Leyla Jael Castro
    orcid: 0000-0003-3986-0510
    affiliation: 6

affiliations:
 - name: ZB MED Information Centre for Life Sciences, Cologne, Germany, and ICESI University, Cali, Colombia
   index: 1
 - name: King Khalid University Department Computer science, Abha, Saudi Arabia
   index: 2
 - name: University of Jeddah Department of Computer Science, Jeddah, Saudi Arabia
   index: 3  
 - name: Imam Abdulrahman Bin Faisal University (IAU), Dammam, Saudi Arabia 
   index: 4
 - name: King Abdullah University of Science and Technology, Thuwal, Saudi Arabia
   index: 5
 - name: ZB MED Information Centre for Life Sciences, Cologne, Germany
   index: 6 
date: 11 February 2023
bibliography: paper.bib
authors_short: Quiñones et al. (2023) Using ontology-based graph embeddings as background knowledge for doc-2-doc similarity
group: Project 13
event: BioHackathon MENA 2023
---

# Introduction

Recommendation systems are an active area of research in Information Retrieval. In the Biomedical domain, the PubMed Recommended Article (PMRA) [@lin_pubmed_2007], a probabilistic approach, is commonly used as a de-facto standard to find articles similar to a reference one. Since it was published in 2007, Natural Language Processing (NLP) has moved forward with the state-of-the-art relying on deep learning approaches. A question arises, is PMRA still a good approach for document similirity or should we look into more state-of-the-art options? The OntoClue project aims at exploring and comparing different approaches, mostly based on word-embeddings but also using lexical pattern matching for Named Entity Recognition (NER). At the BioHackathon MENA 2023, we want to explore the use of document embeddings for document similarity usin background knowledge from ontology-based embeddings.

# Approach

Our approach involves ontology-based embeddings derived from the Medical Subjects Headings (MeSH) vocabulary, a lexical pattenr matching NER, namely Whatizit, and document embeddings combining text and MeSH concepts recognized in the text. As there is no clear gold standard for document-to-document similarity, we have tried out our approach on the RELISH corpus [@relish_corpus_2019], using annotations obtained from Whatizit [@whatizit_2008] as a baseline and correlation to compare variations of the approach to each other. Our approach can be summarized in the following steps:
1. Obtain graph embeddings for the MeSH vocabulary using the [Machine Learning for Ontologies (mOWL) library](https://github.com/bio-ontology-research-group/mowl) [@mowl_2022],
2. Extract MeSH annotations from a pre-annotated version of the RELISH corpus
3. Create document embeddings for each article in the RELISH corpus using two alternatives: (i) aggregate the vectors for all of the MeSH terms recognized in the pre-annotated corpus using the average function, and (ii) create mini-graphs from the MeSH terms recognized in the pre-annotated corpus including closest neighbors, apply graph-embeddings on the mini-graphs and aggregate them per document.
4. Calculate the cosine similarity for all existing pairs in the RELISH corpus
5. Analyze correlation along the three approaches, i.e., lexical matching as baseline, MeSH term vectors from MOWL, and mini-graphs

## Materials
The starting point for our approach is a pre-annotated version of the RELISH corpus with MeSH terms recognized in the text using Whatizit. Whatizit is an automata that takes a dictionary including preferred labels and synonyms for each term in a vocabulary and finds lexical matches with some variations coming from basic regular expresions (e.g., removal of hyphens). The pre-annotated text corresponds to a Tab Separated Values (TSV) file with a first column for the PubMed identifier, a second one for the title and a third one for the abstract. Both title and abstract include MeSH terms (rather than pure text) for any chunck of text where Whatizit recognized a MeSH term. 

## Methods
Initially, the MeSH vocabulary was converted into a graph using mOWL. mOWL is a  library providing different alternatives to create graph embeddings out of ontologies. From the mOWL library, we used the OWL2Vec* [reference link] option to obtain graph embeddings using the mowl.projection function. As a result, we got a file correspoing to a graph version of MeSH, including subclasses, superclasses and other relations. <TODO: File format>

Then we moved to the next step, which was converting the RELISH pre-annotated TSV file to a python dictionary using the JISON library [reference link] and the Load function. Then, we extracted the MeSH terms from the python dictionary using the python library JISON, Pandas, and regular expressions. The next step was calculating the document embeddings, which was done following two alternatives: (i)vectors for MeSH terms from the graph embeddings, and (ii) enrichment of the initial set of MeSH terms recognized in the text using mini-graphs covering close neighbors.

**Document embeddings from graph embeddings.** <TODO: complete this section>

**Document embeddings from enriched mini-graphs.**
<TODO: complete this section>

# Results and Discussion
* We faced a problem with installing the Python Pandas library , and then we solved it by creating a separate environment for the project. 
* Problem with creating the Python dictionary.
* Due to the huge amount of data, the training process is time-consuming hence we used the KAUST cloud.
* DL2Vec did not work well, so we use OWL2Vec.


# Future work

* For the first approach we now on model training phase , after that we need to convert the Python dictionary to vectors using mOWL library functions , then calculate the average between vectors as a way to find the similarities between the articles. we can also use mOWL library functions to Evaluating the embeddings.
*  We found a function on the mWOL library that could convert Meshes to Text (mowl.datasets.builtin) , and we are planning to start working on the second approach on text similraity 

Please remember to introduce tables (see Table 1) before they appear on the document. We recommend to center tables, formulas and figure but not the corresponding captions. Feel free to modify the table style as it better suits to your data.

Table 1
| Header 1 | Header 2 |
| -------- | -------- |
| item 1 | item 2 |
| item 3 | item 4 |

Remember to introduce figures (see Figure 1) before they appear on the document. 

![BioHackrXiv logo](./biohackrxiv.png)
 
Figure 1. A figure corresponding to the logo of our BioHackrXiv preprint.

# Other main section on your manuscript level 1

Feel free to use numbered lists or bullet points as you need.
* Item 1
* Item 2

# Jupyter notebooks, GitHub repositories and data repositories

* https://github.com/zbmed-semtec/mowl-graph2doc2vec

# Acknowledgements
This project was developed as part of the BioHackathon MENA 2023.

LJC is partially funded by NFDI4DS

# References

Leave thise section blank, create a paper.bib with all your references.
