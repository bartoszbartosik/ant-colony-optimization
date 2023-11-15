import numpy as np
import random


def nearest_neighbour(graph: dict):
    """
    Solve graph problem by starting at random node and keep choosing the nearest one until any is left.
    """
    # Unpack graph dictionary
    C, L  = graph.values()
    arcs, values = L.values()

    # Choose random node to start with
    i = np.random.randint(len(C))

    # Initialize solution list
    s = [i]

    # Iterate until s list is not full
    while len(s) < len(C):
        # Initialize lists of feasible nodes for node i
        feasible_arcs = []
        feasible_values = []
        for j in range(len(arcs)):
            # Find connections from node i to j AND which are not present in the s list
            if arcs[j][0] == i and arcs[j][1] not in s[:-1]:
                feasible_arcs.append(arcs[j])
                feasible_values.append(values[j])
                print('arc', arcs[j], 'value', values[j])
        # Get nearest neighbour j
        i = feasible_arcs[np.argmin(np.array(feasible_values))][1]
        s.append(i)
    return s


class AntColonyOptimization:

    def __init__(self, graph, objective_function, ants_number, evaporation_rate, Q):
        self.G = graph
        self.f = objective_function
        self.m = ants_number
        self.ro = evaporation_rate
        self.Q = Q
        self.C = nearest_neighbour()
        self.tau = np.array([])
        self.dtau = np.array([])


    def update_dtau(self):
        pass