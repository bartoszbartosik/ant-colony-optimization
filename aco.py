import numpy as np
import random


def nearest_neighbour(tsp: dict):
    # Solve TSP problem by starting at random city and keep choosing the nearest city until any is left
    # In order to determine C
    components, arcs  = tsp.values()
    arc, values = arcs.values()

    random_component = random.choice(components)
    component_index = np.argwhere(components==random_component)[0][0]
    solution = []

    C = 0
    while len(solution) < len(components):
        feasible_arcs = []
        feasible_values = []
        for i in range(len(arc)):
            if component_index in arc[i] and len(set(arc[i]).intersection(solution)) == 0:
                feasible_arcs.append(arc[i])
                feasible_values.append(values[i])
        solution.append(component_index)
        least_distance = np.argmin(np.array(feasible_values))
        C += feasible_values[least_distance]
        nearest_node = feasible_arcs[least_distance]
        component_index = nearest_node[0] if nearest_node[1] == component_index else nearest_node[1]
        if len(solution) == len(components) - 1:
            solution.append(component_index)
            break
    end_solution = [solution[-1], solution[0]]
    end_solution.sort()
    end_solution = tuple(end_solution)
    idx = arc.index(end_solution)
    C += values[idx]
    return C


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