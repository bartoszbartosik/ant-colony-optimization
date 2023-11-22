import sys

import numpy as np
from matplotlib import pyplot as plt, animation

from aco import AntColonyOptimization as ACO

from tsp import TravelingSalesmanProblem as TSP

def main():

    # Create arrays of cities with their (x, y) coordinates
    cities = np.array([
        [0, 0],     # 0
        [4, 0],     # 1
        [4, 3],     # 2
        [0, 3],     # 3
    ])

    # Randomly generate cities coordinates
    cities_number = 20
    cities = np.array(np.unique(np.random.random(size=(cities_number, 2)), axis=1)*10)
    print(cities)

    # Create TravelingSalesmanProblem instance
    tsp = TSP(cities)

    # Initialize Ant System algorithm
    m = 10
    ro = 0.5
    alpha = 1
    beta = 2
    Q = 1
    aco = ACO(tsp.get_graph(), ants_number=m, evaporation_rate=ro, alpha=alpha, beta=beta, Q=Q)

    # Run algorithm n times to construct ants solutions
    s, value = aco.run(100)
    print(s, value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # #   V I S U A L I S A T I O N   # # # # # # # # # # # # # # # # # # # # # #

    ################################
    ### PREPROCESS OBTAINED DATA ###
    # Optimal solution
    xs = [cities[n][0] for n in s]
    ys = [cities[n][1] for n in s]

    xs.append(xs[0])
    ys.append(ys[0])

    # Paths history
    xh = []
    yh = []

    for h in aco.solutions['s']:
        x = [cities[n][0] for n in h]
        y = [cities[n][1] for n in h]
        x.append(x[0])
        y.append(y[0])
        xh.extend([x])
        yh.extend([y])

    # Pheromones history
    alphas = np.zeros_like(aco.solutions['tau'])
    for t in range(len(alphas)):
        t_min = np.min(aco.solutions['tau'][t])
        t_max = np.max(aco.solutions['tau'][t])
        for i in range(len(alphas[0])):
            for j in range(len(alphas[0][0])):
                if aco.solutions['tau'][t][i][j] <= t_min:
                    alphas[t][i][j] = 0
                elif aco.solutions['tau'][t][i][j] >= t_max:
                    alphas[t][i][j] = 1
                else:
                    alphas[t][i][j] = aco.solutions['tau'][t][i][j]/(t_max-t_min) - t_min/(t_max - t_min)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    #########################
    ### INSTANTIATE PLOTS ###
    # FILENAME
    filename = 'cities-{}_m-{}_ro-{}_a-{}_b-{}_Q-{}'.format(cities_number, m, ro, alpha, beta, Q)

    # CREATE PLOTS
    # Solutions history
    plt.subplot(212)
    plt.plot(aco.solutions['values'], c='0.3')
    plt.title('shortest distance obtained')
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.grid()

    # Cities
    plt.subplot(221)
    plt.scatter(cities[:, 0], cities[:, 1], c='0.25')
    plt.title('cities')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_aspect('equal')
    plt.grid()

    # Cities with optimal path
    plt.subplot(222)
    plt.scatter(cities[:, 0], cities[:, 1], c='0.25')
    plt.plot(xs, ys, c='0.3')
    plt.title('cities and optimal path')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_aspect('equal')
    plt.grid()

    # SAVE PLOT
    plt.gcf().set_size_inches(8, 10)
    plt.savefig("plots/solution-{}.png".format(filename), dpi=200)
    plt.show()

    # ANIMATED PLOT WITH SOLUTION EVOLUTION
    # Plot cities
    fig, ax = plt.subplots()
    ax.scatter(cities[:, 0], cities[:, 1], c='0.25')
    ax_city_links = np.zeros_like(alphas[0], dtype=object)

    # Plot pheromone links between cities
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                ax_city_links[i][j] = ax.plot([cities[i, 0], cities[j, 0]], [cities[i, 1], cities[j, 1]], c='0.5', alpha=0.3, zorder=0)[0]

    # Plot optimal path
    ax_links = ax.plot(xs[0], ys[0], c='0.3', alpha=1)[0]
    iteration_template = 'iteration = %.0f'
    iteration_text = ax.text(0, -0.11, '', transform=ax.transAxes)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.grid()

    # Animation function
    def update(iteration):
        # For each iteration update the optimal path
        x = xh[iteration]
        y = yh[iteration]

        # For each iteration update pheromone trails visibility
        for i in range(len(alphas[0])):
            for j in range(len(alphas[0])):
                if ax_city_links[i][j] != 0:
                    ax_city_links[i][j].set_alpha(alphas[iteration][i][j])

        # Update the optimal path
        ax_links.set_xdata(x)
        ax_links.set_ydata(y)

        # Update text with iteration number
        iteration_text.set_text(iteration_template % (iteration+1))

        return ax_links, ax_city_links

    # Time in milliseconds per frame
    interval = 100

    # Show the plot
    anim = animation.FuncAnimation(fig=fig, func=update, frames=len(xh), interval=interval)
    plt.show()

    # Save animation
    writergif = animation.PillowWriter(fps=len(xh)/interval*10)
    anim.save("plots/tour_construction-{}.gif".format(filename), writer=writergif, dpi=150)

if __name__ == '__main__':
    main()