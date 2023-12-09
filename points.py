"""
This python file contains information about the data point class
and the infected child class. 
"""

import numpy as np
import random


class DataPoint:
    def __init__(self, position,  identifier: int, infectionRange: float, kclusters: int, probInfection: int):
        self.position = position
        self.infectionRange = infectionRange
        self.prob_infection = probInfection
        self.points_in_range = [None]
        self.identifier = identifier
        self.kclusters = kclusters
        self.cluster = None
        self.nearby_clusters = [0] * kclusters


    def calculate_nearby_clusters(self):
        self.nearby_clusters = [0] * self.kclusters
        
        # Counts the number of each cluster type nearby
        for point in self.points_in_range:
            if point is not None:
                cluster = point.cluster
                if cluster is not None:
                    infection = random.uniform(0,1)
                    if infection < self.prob_infection:
                        self.nearby_clusters[cluster] += 1


    # Assigns an uninfected point to a nearby cluster
    def infect(self):

        if not all(cluster_value is 0 for cluster_value in self.nearby_clusters):
            max_cluster = max(self.nearby_clusters)
            if max_cluster is not 0:
                self.cluster = self.nearby_clusters.index(max_cluster)


    # Removes the infection of point
    def uninfect(self):
        self.cluster = None