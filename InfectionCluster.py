"""
This code describes infection clustering, a new clustering method similar
to k-means clustering. 
"""
from points import DataPoint
from point_manager import PointManager

import numpy as np
import math



# This function takes a numpy array, the number of clusters, and some optional hyperparameters and
# returns a numpy array with cluster labels for the data. 

def infection_cluster(Data, kclusters: int = 1, probRecovery: float = 0.4, probInfection: float = 0.2, infectionRange: float = 15, 
                      maxIter: int = 100, verbose: bool = False):
    

    data_point_list = make_data_points(Data, infectionRange, kclusters, probInfection)

    data_pairwise_distances = make_distance_matrix(Data)

    for point in data_point_list:
        get_points_in_range(point, infectionRange, data_pairwise_distances, data_point_list)
    
    # Pass data points to the data manager
    point_manager = PointManager(data_point_list, kclusters, probRecovery)



    # Begin point infection
    point_manager.initial_random_infection(Data)
    point_manager.calculate_cluster_center()
    
    number_of_points_infected = 0
    # Begin infection loop
    for i in range(maxIter):
        if  number_of_points_infected/len(data_point_list)<0.99:
            # Calculates which points should be infected
            for point in point_manager.uninfected_point_list:
                if point != None:
                    point_manager.calculate_infection_clusters(point)
            
            # Infects points
            for point in point_manager.uninfected_point_list:
                if point != None:
                    point_manager.infect_point(point)
                    
            
            point_manager.update_cluster_center()

            
            point_manager.recover_points()

            if verbose == True:
                number_of_points_infected = sum(point_manager.cluster_count_list)
                percent = number_of_points_infected/len(data_point_list)
                print(" %2.2f percent of the points have been clustered." %(percent))

        



    # to reinfect a sufficient number of points: 
    for i in range(int(10/probInfection)):
        for point in point_manager.uninfected_point_list:
            if point != None:
                point_manager.calculate_infection_clusters(point)
        for point in point_manager.uninfected_point_list:
                if point != None:
                    point_manager.infect_point(point)
        point_manager.update_cluster_center()



    # Gives the final number of points that have been infected
    number_of_points_infected = sum(point_manager.cluster_count_list)
    percent = number_of_points_infected/len(data_point_list)
    print(" %2.2f percent of the points have been clustered." %(percent))                

    clustered_data = add_data_clusters(Data, point_manager)


    return clustered_data, point_manager

    




# This function takes the data and changes them to the data point class
def make_data_points(Data, infectionRange, kclusters, probInfection):
    
    data_point_list = []
    for row_index in range(len(Data)):
        position = Data[row_index] #row of numpy array
        intermediate_data = DataPoint(position, row_index, infectionRange, kclusters, probInfection)
        data_point_list.append(intermediate_data)
    
    return data_point_list




# This function creates a matrix containing the pairwise differences of a point with all other points. 
def make_distance_matrix(Data):
    n_points = Data.shape[0]
    distance_matrix = np.zeros((Data.shape[0], Data.shape[0]))

    for i in range(n_points):
            distance_matrix[i, :] = np.linalg.norm(Data - Data[i,:], axis = 1)
    return distance_matrix


# This function calculates the n closest points to each point and saves that information in the point class
def get_points_in_range(point: DataPoint, infection_range: int, distance_matrix, data_point_list):
    point.points_in_range = []
    reference_position = point.identifier

    sorted_distances = np.argsort(distance_matrix[reference_position,:])
    n_closest_indices = sorted_distances[1:infection_range+1]
    for i in n_closest_indices:
        point.points_in_range.append(data_point_list[i]) # To avoid having itself in the closest points

    return 



# This function takes the list of infected data points and adds a column of cluster assignments to the original data
def add_data_clusters(Data, point_manager: PointManager):
    num_rows, num_cols = np.shape(Data)
    new_column = np.zeros((num_rows, 1))
    clustered_data = np.append(Data, new_column, axis = 1)

    for index in range(num_rows):
        point = point_manager.infected_point_list[index]
        if point != None:
            cluster = point.cluster

        else:
            cluster = -1
        clustered_data[index, num_cols] = cluster

    return clustered_data



# This function takes a list of new points and returns the predicted cluster for each. 
def predict_cluster(prediction_points, point_manager: PointManager, method: str = "center"):
    num_rows, num_cols = np.shape(prediction_points)
    new_column = np.zeros((num_rows, 1))
    clustered_data = np.append(prediction_points, new_column, axis = 1)

    
    # Fix this one
    if method == "center":
        for index in range(num_rows):
            # Calculates distances to the centers of the clusters
            center_distances = np.linalg.norm(prediction_points[index] - np.array(point_manager.cluster_center_list), axis = 0)
            closest_center = center_distances.index(min(center_distances))

            clustered_data[index, num_cols] = closest_center
    
    # TODO: Add an infection-based prediction method
    # if method == "infect":


    return clustered_data

