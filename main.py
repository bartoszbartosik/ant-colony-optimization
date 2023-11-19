import sys

import numpy as np

from aco import AntColonyOptimization as ACO

from tsp import TravelingSalesmanProblem as TSP

def main():

    # Create arrays of cities with their (x, y) coordinates
    cities = np.array([
        [0, 0],     # 0
        [4, 0],     # 1
        [4, 3],     # 2
        [0, 3],     # 3
    ])

    # Create TravelingSalesmanProblem instance
    tsp = TSP(cities)

    # Compute distance between given series of cities
    sample_path = np.array([0, 2, 1, 3])
    print(tsp.get_distance(sample_path))

    # Initialize Ant System algorithm
    aco = ACO(tsp.get_graph(), tsp.get_distance, ants_number=10, evaporation_rate=0.5, alpha=1, beta=3, Q=1)
    # Run algorithm n times to construct ants solutions
    aco.run(10)
    # Predict solution starting from given node
    print(aco.predict(0))



if __name__ == '__main__':
    main()