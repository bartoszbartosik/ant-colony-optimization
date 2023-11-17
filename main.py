import numpy as np

import aco
from aco import AntColonyOptimization as ACO

def main():

    def objective_function(path):
        _, arcs = tsp.values()
        links, distances = arcs.values()

        total_distance = 0
        for i in range(len(path)):
            link = tuple([path[i-1], path[i]])
            idx = links.index(link)
            total_distance += distances[idx]
        return total_distance


    cities = np.array([
        [0, 0],     # 0
        [4, 1],     # 1
        [6, 4],     # 2
        [8, 2],     # 3
        [2, 4],     # 4
    ])
    sample_path = np.array([0, 2, 4, 3, 1])

    tsp = {
        'components': cities,
        'arcs': {
            'arc': [],
            'value': []
        }
    }

    for i in range(len(cities)):
        for j in range(len(cities)):
            # if i >= j:
            if i == j:
                    continue
            tsp['arcs']['arc'].append((i, j))
            tsp['arcs']['value'].extend([np.sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2)])

    print(tsp['components'], tsp['arcs'])
    print(objective_function(sample_path))

    aco = ACO(tsp, objective_function, ants_number=10, evaporation_rate=0.5, alpha=1, beta=3, Q=1)
    aco.tau_init()
    print(aco.nearest_neighbour())
    print(aco.tour_construction())


if __name__ == '__main__':
    main()