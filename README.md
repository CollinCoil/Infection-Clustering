[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/CollinCoil/Infection-Clustering)

# Infection Clustering

Infection clustering is an unsupervised machine learning technique for data clustering. The goal is to simulate the behavior of an infectious disease passing through a population. In this case, the data points are the population of interest, and the clusters are the infection. Points get exposed to an infection based on their proximity to infected points, and the infected points have a chance to recover. This mechanism of iteratively infecting and uninfecting the data allows the clustering algorithm to effectively cluster data. The paper in this repo provides a description of the algorithm and discussess some mathematical theorems guiding development of this program. 

## Usage
To use infection clustering on data, import it with 
```python
from InfectionCluster import *
```

Additional functionality is being developed for making cluster predictions using infection clustering. 

## Citation
If you use Infection Clustering, please cite

@misc{Infection-cluster,  
author = {Collin Coil},  
title = {{Infection Clustering}},  
howpublished = {\url{https://github.com/CollinCoil/Infection-Clustering }}  
}
