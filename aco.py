import numpy as np


class AntColonyOptimization:

    def __init__(self, cities, objective_function, ants_number, evaporation_rate, Q):
        self.f = objective_function
        self.m = ants_number
        self.ro = evaporation_rate
        self.Q = Q
        self.tau = np.array([])
        self.dtau = np.array([])


    def update_dtau(self):
        pass