import numpy as np

import aco as ACO

def main():

    def objective_function(cities, path):
        sum = 0
        for i in range(len(path))[1:]:
            sum += np.sqrt((cities[path[i]][0] - cities[path[i-1]][0])**2 + (cities[path[i]][1] - cities[path[i-1]][1])**2)
        sum += np.sqrt((cities[path[-1]][0] - cities[path[0]][0])**2 + (cities[path[-1]][1] - cities[path[0]][1])**2)
        return sum


    cities = np.array([
        [0, 0],     # 0
        [4, 1],     # 1
        [6, 4],     # 2
        [8, 2],     # 3
        [2, 4],     # 4
    ])


    sample_path = np.array([0, 2, 4, 3, 1])

    print(objective_function(cities, sample_path))


if __name__ == '__main__':
    main()