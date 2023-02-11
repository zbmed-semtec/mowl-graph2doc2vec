# mowl-graph2doc2vec
A repository to explore the use of ontology-based graphs (generated with MOWL) as background knowledge for scientific articles similarity. 
# Materials and libraries
* [RELISH](https://doi.org/10.1093/database/baz085) [corpus](https://figshare.com/projects/RELISH-DB/60095)
* RELISH corpus pre-annotated with terms from the [MeSH vocabulary](https://www.nlm.nih.gov/mesh/meshhome.html) provided by ZB MED
* [MOWL library](https://github.com/bio-ontology-research-group/mowl) to generate graphs from ontologies
* Libraries to create graph embeddings
 
# Plan for the BioHackathon MENA 2023
1. Using MOWL to generate a graph corresponding to the MeSH vocabulary. The input for this step is the MeSH vocabulary and the output is a graph.
2. Using the RELISH corpus pre-annotated with MeSH terms (i.e., any entity from the MeSH vocabulary recognized in the text will have been replaced by the corresponding term ID) create a mini-graph for each document. Use co-occurrence to add weights to the edges. This graph will be most likely kind of disconnected (e.g., not too many edges). The input for this step will be a TSV file where each row is a pre-annotated article from the RELISH corpus (see example below) while the output will be a graph per document.
3. For all nodes in a document mini-graph, identify the direct nodes coming from the MeSH-based graph and add them to the mini-graph. This will give you a  more connected graph, with background knowledge coming from the MeSH vocabulary. The inputs for this step are the document mini-graphs while the outputs will be document enriched mini-graphs.
4. Create graph embeddings for the documents in the RELISH corpus.
5. Calculate the cosine similarity for each existing pair of documents in the corpus.
6. Analyze correlation of the cosine similarities using this approach versus another one created in the OntoClue framework.
7. Discuss results (lessons learnt, possible variations, limitations).


## Pre-annotated RELISH corpus
| PMID | title | abstract |
| --- | --- | --- |
| 10821866 | meshd003643 signal-induced localization of p53 meshd011506 to meshd008928 a potential meshd012380 in apoptotic signaling | the mechanism of p53-mediated meshd017209 after cellular stress remains poorly understood evidence suggests that p53 induces meshd016923 by a multitude of molecular pathways involving activation of target meshd005796 and transcriptionally independent direct signaling meshd008928 meshd010988 a key meshd012380 in meshd017209 we show here that a fraction of p53 meshd011506 localizes to meshd008928 at the onset of p53-dependent meshd017209 but not during p53-independent meshd017209 or p53-mediated meshd059447 the accumulation of p53 to meshd008928 is rapid within 1 h after p53 activation and precedes changes in meshd053078 meshd045304 release and meshd053148 activation meshd016253 and immuno-meshd005453-activated meshd002477 sorter meshq000032 of isolated meshd008928 show that the majority of mitochondrial p53 localizes to the membranous compartment whereas a fraction is found in a complex with the mitochondrial import motor mt hsp70 after induction of ectopic p53 without additional meshd004249 in p53-deficient meshd002477 p53 again partially localizes to meshd008928 preceding the onset of meshd017209 overexpression of anti-apoptotic bcl-2 or bcl-xl abrogates stress signal-mediated mitochondrial p53 accumulation and meshd017209 but not meshd059447 suggesting a meshd005246 signaling loop between p53 and mitochondrial apoptotic regulators importantly bypassing the nucleus by targeting p53 to meshd008928 using import leader fusions is sufficient to induce meshd017209 in p53-deficient meshd002477 we propose a model where p53 can contribute to meshd017209 by direct signaling at the meshd008928 thereby amplifying the transcription-dependent meshd017209 of p53 | 

## Limitations
* We are not capturing relations from the text between two recognized.
* Some biologically relevant entities, see P53 in the example, are not part of the MeSH vocabulary (however this approach is for a recommendation system and not for a specific biological task so might still be ok).

## Ideas for the future
* Explore Named Entity Recognition approaches other than simple/direct lexical matching.
* Using sentiment analysis to add positive/negative connotation to the relation betweeen two entities recognized in the text.

## Participants
* Nelson David Quiñones Virgen, co-lead, orcid:0000-0002-5037-0443
* Leyla Jael Castro, co-lead, orcid:0000-0003-3986-0510
* Asmaa Alqhtani, participant, orcid:0000-0002-3119-5109 
* Rahaf Alayed, participant, orcid: 
* Layan Aljohani, participant, orcid:0000-0001-6954-2973 
* Maria G Gomez Castillo, participant, orcid: 


## BioHackathon diary
* Day 1: Formation of the team, discussion on the approach, distribution of initial tasks. 
  * Task 1: Asmaa, Rahaf, Layan, Maria. Getting a graph out of MeSH using mOWL
  * Task 2: Nelson. Explore strategies to create mini-graphs representing the publications
* Day 2
  * Task 1 done, using the KAUST cloud, output saved in a pkl file, the projection used was DL2Vec for taxonomy only in two directions.
  * Task 2: MeSH terms extracted to a JSON file using the PMID as key for each article, invlufinh the co-occurrence count. 
  * Task 3: Maria and Rahaf. From the MeSH graph created in Task 1, use a graph embedding algorithm to obtain the graph embeddings, each concept will be assigned a vector
  * Task 4a: Layan and Maria. Define and implement a strategy to get all the concept embeddings for a document and move to document embeddings. Once the MeSH graph embeddings are ready, apply to the actual data.
  * Task 4b: Nelson. Define and implement a strategy to create mini-graphs out the concepts identified in each document and the MeSH graph embeddings.
* Day 3
  * Leyla Jael. Add information to the mid-term report. Done
  * Task 4a. Asma, Rahaf, Maria, Layan. Word embeddings for the graph are done. Continuing with the document embeddings for RELISH corpus.
  * Task 4b. Nelson. Exploring options based on lowest common ancestor.


# Acknowledgments
This project started as part of the BioHackathon MENA 2023
