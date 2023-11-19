import sys

import numpy as np


class TravelingSalesmanProblem:

    def __init__(self, cities):
        self.cities = cities
        self.distances = np.zeros(shape=(len(cities), len(cities)))
        for i in range(len(cities)):
            for j in range(len(cities)):
                if i == j:
                    self.distances[i][j] = sys.maxsize
                    continue
                self.distances[i][j] = np.sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2)


    def get_distance(self, path):
        total_distance = 0
        for i in range(len(path)):
            total_distance += self.distances[path[i-1], path[i]]
        return total_distance

    def get_graph(self):
        return self.cities, self.distances