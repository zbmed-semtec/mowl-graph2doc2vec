## Instructions to run the algorithms.


To execute this algorithms for the first time you need to create a conda environment. Conda is a powerful package manager and environment manager.

Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). 


Enter the Code folder in the terminal window.
Then execute the following command on the terminal.

```
conda env create -f environment.yml
```

In the environment.yml file we specify all the necessary libraries or software that is required to run the project.

After the enviroment is created every time you want to work on the project you need to activate it.

```
conda activate graph2doc2vec_env
```

In case updates have been preformed on the environment.yml file you need to update the dependencies with.

```
conda env update graph2doc2vec_env --file environment.yml --prune
```




*Graph_With_Cooccurrences: The algorithm generates links between 2 MESH concepts in a paragraph based on how many times the 2 terms appear in a sentence. Then an edge between the x% of the most coocurrent pairs is made.
