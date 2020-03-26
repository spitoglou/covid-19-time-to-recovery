# covid-19-time-to-recovery

[![DOI](https://zenodo.org/badge/248425825.svg)](https://zenodo.org/badge/latestdoi/248425825)

This repository contains the code of the calculations described in the paper: "__A Method of Estimating Time-to-Recovery for a Disease Caused by a Contagious Pathogen like SARS-CoV-2 using a Time Series of Aggregated Case Reports__"

Authors: Stavros Pitoglou [1, 2], Dimitrios-Dionysios Koutsouris [1]

_[1] Biomedical Engineering Laboratory, National Technical University of Athens, Athens, Greece_   
_[2] Research & Development, Computer Solutions SA, Athens, Greece_

The original paper's reported results reside in the folder ```paper_results```

### Setting up environment

#### Anaconda

Anaconda is a free distribution of the Python programming language for large-scale data processing, predictive analytics, and scientific computing that aims to simplify package management and deployment.

Follow instructions to install [Anaconda](https://docs.continuum.io/anaconda/install) or the more lightweight [miniconda](http://conda.pydata.org/miniconda.html).

#### Conda packages
In the root of the project there is a platform independent ```environmnet.yml``` file.

You can find up-to-date instructions on how to install and activate it [here (conda documentation)](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

### Usage
#### Calculations
First navigate to the project's folder.  
Then:
```python
conda activate covidttr
python covidttr.py
``` 
#### Notebooks
```
jupyter notebook
```
```Stavros Pitoglou, March 2020```
