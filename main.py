import sys

import numpy as np
from matplotlib import pyplot as plt

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

    cities = np.array([
        [21.02, 52.12],
        [22.34, 51.14],
        [19.30, 49.53],
        [17.02, 51.07],
        [19.02, 54.02],
        [14.26, 53.56],
        [18.38, 54.22],
        [18.32, 54.32],
        [22.01, 50.03],
        [16.55, 52.25],
        [19.00, 50.15],
        [20.37, 50.53],
        [19.57, 50.03],
        [17.56, 50.40],
        [23.10, 53.08],
        [19.04, 49.50],
        [16.22, 52.14],
        [14.34, 53.26],
        [15.30, 51.56],
        [18.00, 53.07],
    ])

    # Create TravelingSalesmanProblem instance
    tsp = TSP(cities)

    # Compute distance between given series of cities
    sample_path = np.array([0, 2, 1, 3])
    print(tsp.get_distance(sample_path))

    # Initialize Ant System algorithm
    aco = ACO(tsp.get_graph(), ants_number=10, evaporation_rate=0.5, alpha=1, beta=3, Q=1)
    # Run algorithm n times to construct ants solutions
    aco.run(500)
    # Predict solution starting from given node
    s, value = aco.get_solution()
    print(s, value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # #   V I S U A L I S A T I O N   # # # # # # # # # # # # # # # # # # # # # #
    xs = [cities[n][0] for n in s]
    ys = [cities[n][1] for n in s]

    xs.append(xs[0])
    ys.append(ys[0])

    plt.subplot(121)
    plt.scatter(cities[:, 0], cities[:, 1])
    plt.grid()

    plt.subplot(122)
    plt.scatter(cities[:, 0], cities[:, 1])
    plt.plot(xs, ys)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()