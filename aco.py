import sys

import numpy as np
from ant import Ant
import random


class AntColonyOptimization:

    def __init__(self, graph: dict, objective_function, ants_number: int, evaporation_rate: float, alpha, beta, Q):
        # Unpack graph values
        self.C, self.L = graph.values()
        self.arcs, self.values = self.L.values()
        # # #
        self.f = objective_function
        self.m = ants_number
        self.ro = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        # # #
        # Inner variables
        self.ants = [Ant() for i in range(ants_number)]
        self.tau = np.zeros_like(list(list(graph.values())[1].values())[1])
        self.dtau = np.array([])


    def tour_construction(self):
        nodes = range(len(self.C))
        for ant in self.ants:
            ant.M.append(random.choice(nodes))
            self.select_next_node(ant.M[-1])


    def select_next_node(self, i):
        # Current node
        s = [i]

        feasible_indexes = []
        for j in range(len(self.arcs)):
            # Find connections from node i to j AND which are not present in the s list
            if self.arcs[j][0] == i and self.arcs[j][1] not in s[:-1]:
                feasible_indexes.append(j)

        print('feasible_nodes', feasible_indexes)
        [print(self.arcs[i]) for i in feasible_indexes]
        # Get nearest neighbour j
        s.append(i)


    def tau_init(self):
        L = self.f(self.nearest_neighbour())
        self.tau += self.m/L


    def nearest_neighbour(self):
        """
        Solve graph problem by starting at random node and keep choosing the nearest one until any is left.
        """
        # Choose random node to start with
        i = np.random.randint(len(self.C))

        # Initialize solution list
        s = [i]

        # Iterate until s list is not full
        while len(s) < len(self.C):
            # Initialize lists of feasible nodes for node i
            nearest_index = 0
            nearest_value = sys.maxsize
            for j in range(len(self.arcs)):
                # Find connections from node i to j AND which are not present in the s list
                if self.arcs[j][0] == i and self.arcs[j][1] not in s[:-1]:
                    if self.values[j] < nearest_value:
                        nearest_value = self.values[j]
                        nearest_index = j
            # Get nearest neighbour j
            i = self.arcs[nearest_index][1]
            s.append(i)

        return s