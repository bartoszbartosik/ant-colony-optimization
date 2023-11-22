import sys

import numpy as np
from ant import Ant
import random


class AntColonyOptimization:

    def __init__(self, graph: tuple, ants_number: int, evaporation_rate: float, alpha, beta, Q):
        # Unpack graph values
        self.__C, self.__L = graph
        # # #
        self.__m = ants_number
        self.__ro = evaporation_rate
        self.__alpha = alpha
        self.__beta = beta
        self.__Q = Q
        # # #
        # Inner variables
        self.__ants = []
        self.__eta = 1 / np.array(self.__L)
        self.__tau = np.zeros_like(self.__L)
        self.__tau_init()

        self.solutions = {
            's': [],
            'values': [],
            'tau': []
        }


    def run(self, iterations) -> tuple:
        """
        Run algorithm specified number of times.
        Returns permutation of nodes corresponding to the optimal solution.
        """
        for i in range(iterations):
            # Show progress bar
            sys.stdout.write('\r')
            sys.stdout.write("Ants path construction in progress: [%-20s] %d%%" % ('=' * int(i / iterations * 20), int(i / iterations * 100)))
            sys.stdout.flush()
            # Spawn new ants
            self.__ants = [Ant() for _ in range(self.__m)]

            # Construct tour for each ant
            solution, value = self.__tour_construction()
            # Append the one which did best to the solutions
            self.solutions['s'].append(solution)
            self.solutions['values'].append(value)

            # Update pheromone trails
            self.__update_pheromones()

        min_value = min(self.solutions['values'])
        best_solution = self.solutions['s'][self.solutions['values'].index(min_value)]
        return best_solution, min_value


    def __update_pheromones(self):
        """
        Update and save tau matrix using pheromone evaporation parameter 'ro', and solution constructed by ants using parameter 'Q' and length of the tour they traveled.
        """
        self.__tau *= (1 - self.__ro)

        for ant in self.__ants:
            path = ant.M
            for i in range(len(ant.M)):
                self.__tau[path[i - 1], path[i]] += self.__Q / ant.L
        self.solutions['tau'].append(self.__tau.copy())


    def __tour_construction(self) -> tuple:
        """
        Create ant solutions. Each ant starts at randomly chosen node and selects the next one parallely with other ants.
        After ants finish their tours, the one which path was the shortest is selected in order to return its permutation of visited nodes, and the length of the tour it traveled.
        """
        min_value = sys.maxsize
        solution = 0

        nodes = len(self.__C)
        for node in range(nodes-1):
            for ant in self.__ants:
                if len(ant.M) == 0:
                    ant.M.append(random.choice(range(nodes)))
                j = self.__select_next_node(ant.M)
                ant.M.append(j)
                ant.L += self.__L[ant.M[-2], j]
                if node == nodes - 2:
                    ant.L += self.__L[ant.M[0], ant.M[-1]]
                    if ant.L < min_value:
                        min_value = ant.L
                        solution = ant.M
        return solution, min_value


    def __select_next_node(self, M):
        """
        For the given list of nodes, choose the next one and return its index.
        """
        # Current node
        i = M[-1]

        feasible_nodes = []
        p = np.array([])
        for j in range(len(self.__L[i])):
            # Consider j which are not present in the M list
            if j not in M[:-1]:
                feasible_nodes.append(j)
                p_ij = self.__tau[i][j] ** self.__alpha * self.__eta[i][j] ** self.__beta
                p = np.append(p, p_ij)

        p = p/sum(p)
        j = np.random.choice(feasible_nodes, p=p)

        return j


    def __tau_init(self):
        """
        Initialize tau matrix using nearest neighbour heuristic.
        """
        _, L = self.nearest_neighbour()
        self.__tau += self.__m / L


    def nearest_neighbour(self) -> tuple:
        """
        Solve graph problem by starting at random node and keep choosing the nearest one until any is left.
        Returns tuple consisting of nodes permutation and its value for the given problem.
        """
        # Initialize solution list with randomly chosen node
        s = [np.random.randint(len(self.__C))]

        # Iterate until s list is not full
        while len(s) < len(self.__C):
            # Current node
            i = s[-1]

            # Initialize lists of feasible nodes for node i
            nearest_index = 0
            nearest_value = sys.maxsize

            # Consider all j nodes linked to i
            for j in range(len(self.__L[i])):
                # Consider j which are not present in the s list
                if j not in s[:-1]:
                    if self.__L[i][j] < nearest_value:
                        nearest_value = self.__L[i][j]
                        nearest_index = j

            # Get nearest neighbour j
            s.append(nearest_index)

        total_value = 0
        for i in range(len(s)):
            total_value += self.__L[s[i - 1], s[i]]

        return s, total_value