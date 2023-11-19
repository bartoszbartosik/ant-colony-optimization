import sys

import numpy as np
from ant import Ant
import random


class AntColonyOptimization:

    def __init__(self, graph: tuple, objective_function, ants_number: int, evaporation_rate: float, alpha, beta, Q):
        # Unpack graph values
        self.C, self.L = graph
        # # #
        self.f = objective_function
        self.m = ants_number
        self.ro = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        # # #
        # Inner variables
        self.ants = []
        self.eta = 1/np.array(self.L)
        self.tau = np.zeros_like(self.L)


    def predict(self, starting_node):
        nodes = len(self.C)
        ant = Ant()
        ant.M.append(starting_node)
        for node in range(nodes - 1):
            j = self.select_next_node(ant.M)
            ant.M.append(j)
            ant.L += self.L[ant.M[-2], j]
            if node == nodes - 2:
                ant.L += self.L[ant.M[0], ant.M[-1]]
        return ant.M, ant.L


    def run(self, iterations):
        self.tau_init()
        for _ in range(iterations):
            self.ants = [Ant() for _ in range(self.m)]
            self.tour_construction()
            self.update_pheromones()

    def update_pheromones(self):
        self.tau *= (1-self.ro)

        for ant in self.ants:
            path = ant.M
            for i in range(len(ant.M)):
                self.tau[path[i - 1], path[i]] += self.Q/ant.L

            ant.M = []
            ant.L = 0

        print(self.tau)


    def tour_construction(self):
        nodes = len(self.C)
        for node in range(nodes-1):
            for ant in self.ants:
                if len(ant.M) == 0:
                    ant.M.append(random.choice(range(nodes)))
                j = self.select_next_node(ant.M)
                ant.M.append(j)
                ant.L += self.L[ant.M[-2], j]
                if node == nodes - 2:
                    ant.L += self.L[ant.M[0], ant.M[-1]]

        for ant in self.ants:
            print('nodes:', ant.M, 'distances:', ant.L)


    def select_next_node(self, M):
        # Current node
        i = M[-1]

        feasible_nodes = []
        p = np.array([])
        for j in range(len(self.L[i])):
            # Find connections from node i to j AND which are not present in the s list
            if j not in M[:-1]:
                feasible_nodes.append(j)
                p_ij = self.tau[i][j]**self.alpha * self.eta[i][j]**self.beta
                p = np.append(p, p_ij)

        p = p/sum(p)
        j = np.random.choice(feasible_nodes, p=p)

        return j


    def tau_init(self):
        s, L = self.nearest_neighbour()
        self.tau += self.m/L


    def nearest_neighbour(self):
        """
        Solve graph problem by starting at random node and keep choosing the nearest one until any is left.
        """
        # Initialize solution list with randomly chosen node
        s = [np.random.randint(len(self.C))]

        # Iterate until s list is not full
        while len(s) < len(self.C):
            # Current node
            i = s[-1]

            # Initialize lists of feasible nodes for node i
            nearest_index = 0
            nearest_value = sys.maxsize

            # Consider all j nodes linked to i
            for j in range(len(self.L[i])):
                # Consider j which are not present in the s list
                if j not in s[:-1]:
                    if self.L[i][j] < nearest_value:
                        nearest_value = self.L[i][j]
                        nearest_index = j

            # Get nearest neighbour j
            s.append(nearest_index)

        total_value = 0
        for i in range(len(s)):
            total_value += self.L[s[i-1], s[i]]

        return s, total_value