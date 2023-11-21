import sys

import numpy as np
from ant import Ant
import random


class AntColonyOptimization:

    def __init__(self, graph: tuple, ants_number: int, evaporation_rate: float, alpha, beta, Q):
        # Unpack graph values
        self.C, self.L = graph
        # # #
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
        self.tau_init()

        self.solutions = {
            's': [],
            'values': [],
            'tau': []
        }


    def run(self, iterations):
        solution, value = 0, 0
        for i in range(iterations):
            # Show progress bar
            sys.stdout.write('\r')
            sys.stdout.write("Ants path construction in progress: [%-20s] %d%%" % ('=' * int(i / iterations * 20), int(i / iterations * 100)))
            sys.stdout.flush()
            # Spawn new ants
            self.ants = [Ant() for _ in range(self.m)]

            # Construct tour for each ant
            solution, value = self.tour_construction()
            # Append the one which did best to the solutions
            self.solutions['s'].append(solution)
            self.solutions['values'].append(value)

            # Update pheromone trails
            self.update_pheromones()

        min_value = min(self.solutions['values'])
        best_solution = self.solutions['s'][self.solutions['values'].index(min_value)]
        return best_solution, min_value


    def update_pheromones(self):
        self.tau *= (1-self.ro)

        for ant in self.ants:
            path = ant.M
            for i in range(len(ant.M)):
                self.tau[path[i - 1], path[i]] += self.Q/ant.L
        self.solutions['tau'].append(self.tau.copy())


    def tour_construction(self):
        min_value = sys.maxsize
        solution = 0

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
                    if ant.L < min_value:
                        min_value = ant.L
                        solution = ant.M
        return solution, min_value


    def select_next_node(self, M):
        # Current node
        i = M[-1]

        feasible_nodes = []
        p = np.array([])
        for j in range(len(self.L[i])):
            # Consider j which are not present in the M list
            if j not in M[:-1]:
                feasible_nodes.append(j)
                p_ij = self.tau[i][j]**self.alpha * self.eta[i][j]**self.beta
                p = np.append(p, p_ij)

        p = p/sum(p)
        j = np.random.choice(feasible_nodes, p=p)

        return j


    def tau_init(self):
        _, L = self.nearest_neighbour()
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