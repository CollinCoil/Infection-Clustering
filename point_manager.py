"""
This file contains the code for the data manager that tracks all data, the infected data, and the uninfected data
"""

import numpy as np
import random
import math
import sys




class PointManager:
    def __init__(self, data_point_list: list, kclusters: int, probRevocery: int):
        # Data Lists
        self.uninfected_point_list = data_point_list
        self.infected_point_list = [None] * len(data_point_list)
        self.kclusters = kclusters

        # Cluster Count Information
        self.cluster_count_list = [1] * kclusters    # Starts at 1 for initial infection points

        # Additional Information
        self.prob_recovery = probRevocery



    def calculate_infection_clusters(self, point):
        if point.cluster is None:
            point.calculate_nearby_clusters()




    def infect_point(self, point, cluster = None):
        if cluster is None:
            # Infects the points based on nearby points
            if point.cluster is None:
                point.infect()

        else: 
            point.cluster = cluster

        if point.cluster is not None:
            # Increases the point cluster counter
            self.cluster_count_list[point.cluster] += 1

            # Add the point to the infected point list
            self.infected_point_list[point.identifier] = point

            # Remove the point from the uninfected point list
            self.uninfected_point_list[point.identifier] = None



    def uninfect_point(self, point):
        # Decreases the point cluster counter
        self.cluster_count_list[point.cluster] -= 1

        # Uninfects the point
        point.uninfect()

        # Add the point to the uninfected point list
        self.uninfected_point_list[point.identifier] = point

        # Remove the point from the infected point list
        self.infected_point_list[point.identifier] = None



    def initial_random_infection(self, data):
        # Initialize the centroids list and add a randomly selected data point to the list
        centroids = []
        random_index = np.random.randint(data.shape[0])
        centroids.append(data[random_index, :])

        # Assign point to cluster 0
        point = self.uninfected_point_list[random_index]
        point.cluster = 0
        
        # Add the point to the infected point list
        self.infected_point_list[point.identifier] = point 

        # Remove the point from the uninfected point list
        self.uninfected_point_list[point.identifier] = None

    
        # Compute remaining k - 1 centroids
        for c_id in range(self.kclusters - 1):

            # Initialize a list to store distances of data points from nearest centroid
            dist = []
            for i in range(data.shape[0]):
                point = data[i, :]
                d = sys.maxsize

                # Compute distance of 'point' from each of the previously selected centroid and store the minimum distance
                for j in range(len(centroids)):
                    difference = point - centroids[j]
                    temp_dist = np.linalg.norm(difference)
                    d = min(d, temp_dist)
                dist.append(d)

            # Select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_index = np.argmax(dist)
            next_centroid = data[next_index, :]
            centroids.append(next_centroid)
            dist = []

            # Assign point to cluster
            point = self.uninfected_point_list[next_index]
            point.cluster = c_id + 1


            # Add the point to the infected point list
            self.infected_point_list[next_index] = point

            # Remove the point from the uninfected point list
            self.uninfected_point_list[next_index] = None
    
    
    
    # This method calculates the center of each cluster
    def calculate_cluster_center(self):
        coordinate_tuple = tuple(point.position for point in self.infected_point_list if point != None)
        coordinate_array = np.vstack((coordinate_tuple))
        self.cluster_center_list = np.mean(coordinate_array, axis = 0)




    # This method calculates the new center of each cluster and the change from previous
    def update_cluster_center(self):
        self.calculate_cluster_center()


    # This function takes the list of infected points and recovers some of them
    def recover_points(self):
        for point in self.infected_point_list: 

            if point != None:
                cluster = point.cluster
                recovery = random.uniform(0,1)

                if recovery < self.prob_recovery:
                    self.uninfect_point(point)

                if self.cluster_count_list[cluster] < 1: # randomly moving the infection to a different point if infection is eliminated
                    random_point = None
                    while random_point is None:
                        random_point_list = random.sample(self.uninfected_point_list, 1)
                        random_point = random_point_list[0]

                    self.infect_point(random_point, cluster)
