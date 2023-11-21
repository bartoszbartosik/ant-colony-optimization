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

    cities = np.array(np.unique(np.random.random(size=(50, 2)), axis=1)*10)
    print(cities)

    # Create TravelingSalesmanProblem instance
    tsp = TSP(cities)

    # Compute distance between given series of cities
    sample_path = np.array([0, 2, 1, 3])
    print(tsp.get_distance(sample_path))

    # Initialize Ant System algorithm
    aco = ACO(tsp.get_graph(), ants_number=10, evaporation_rate=0.5, alpha=1, beta=2, Q=1)

    # Run algorithm n times to construct ants solutions
    s, value = aco.run(10)
    print(s, value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # #   V I S U A L I S A T I O N   # # # # # # # # # # # # # # # # # # # # # #
    xs = [cities[n][0] for n in s]
    ys = [cities[n][1] for n in s]

    xs.append(xs[0])
    ys.append(ys[0])

    plt.subplot(212)
    plt.plot(aco.solutions['values'], c='0.3')
    plt.title('shortest distance obtained')
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.grid()

    plt.subplot(221)
    plt.scatter(cities[:, 0], cities[:, 1], c='0.25')
    plt.title('cities')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_aspect('equal')
    plt.grid()

    plt.subplot(222)
    plt.scatter(cities[:, 0], cities[:, 1], c='0.25')
    plt.plot(xs, ys, c='0.3')
    plt.title('cities and optimal path')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_aspect('equal')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()