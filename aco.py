import numpy as np
import random


class AntColonyOptimization:

    def __init__(self, graph: dict, objective_function, ants_number: int, evaporation_rate: float, Q):
        # Unpack graph values
        self.C, self.L = graph.values()
        self.arcs, self.values = self.L.values()
        # # #
        self.f = objective_function
        self.m = ants_number
        self.ro = evaporation_rate
        self.Q = Q
        # # #
        # Inner variables
        self.tau = np.zeros_like(list(list(graph.values())[1].values())[1])
        self.dtau = np.array([])


    def tour_construction(self):
        pass


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
            feasible_arcs = []
            feasible_values = []
            for j in range(len(self.arcs)):
                # Find connections from node i to j AND which are not present in the s list
                if self.arcs[j][0] == i and self.arcs[j][1] not in s[:-1]:
                    feasible_arcs.append(self.arcs[j])
                    feasible_values.append(self.values[j])
            # Get nearest neighbour j
            i = feasible_arcs[np.argmin(np.array(feasible_values))][1]
            s.append(i)
        return s