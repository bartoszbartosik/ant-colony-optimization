import numpy as np

import aco as ACO

def main():

    def objective_function(tsp, path):
        _, links, distances = tsp.values()

        total_distance = 0
        for i in range(len(path)):
            link = [path[i-1], path[i]]
            link.sort()
            link = tuple(link)
            idx = links.index(link)
            total_distance += distances[idx]
            print('link:', link, 'idx:', idx, 'distance:', distances[idx])
        return total_distance


    cities = np.array([
        [0, 0],     # 0
        [4, 1],     # 1
        [6, 4],     # 2
        [8, 2],     # 3
        [2, 4],     # 4
    ])
    sample_path = np.array([0, 2, 4, 3, 1])

    tsp = {
        'cities': cities,
        'links': [],
        'distances': np.array([])
    }

    for i in range(len(cities)):
        for j in range(len(cities)):
            if i >= j:
                continue
            tsp['links'].append((i,j))
            tsp['distances'] = np.append(tsp['distances'], np.sqrt((cities[i][0] - cities[j][0])**2 + (cities[i][1] - cities[j][1])**2))

    print(tsp['links'], tsp['distances'])


    print(objective_function(tsp, sample_path))


if __name__ == '__main__':
    main()