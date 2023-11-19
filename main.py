import sys

import numpy as np

import aco
from aco import AntColonyOptimization as ACO

def main():

    def objective_function(path):
        components, values = tsp

        total_distance = 0
        for i in range(len(path)):
            total_distance += values[path[i-1], path[i]]
        return total_distance

    cities = np.array([
        [0, 0],     # 0
        [4, 0],     # 1
        [4, 3],     # 2
        [0, 3],     # 3
    ])
    sample_path = np.array([0, 2, 1, 3])

    distances = np.zeros(shape=(len(cities), len(cities)))
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i == j:
                distances[i][j] = sys.maxsize
                continue
            distances[i][j] = np.sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2)

    print(distances)
    tsp = (cities, distances)

    print(objective_function(sample_path))

    aco = ACO(tsp, objective_function, ants_number=10, evaporation_rate=0.5, alpha=1, beta=3, Q=1)
    aco.tau_init()
    print(aco.tour_construction())



if __name__ == '__main__':
    main()