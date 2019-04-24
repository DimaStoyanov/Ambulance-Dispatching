from common import *
from simulation.stats.ChangeStrategyEquilibriumStats import ChangeStrategyEquilibriumStats

def change_strategy_plot(start_strategies='AAA', points=4):
    payoff_matrix = np.zeros((points,points))
    for la in np.linspace(12, 14, points):
        for mu in np.linspace(120, 124, points):
            stats = ChangeStrategyEquilibriumStats(la, mu, start_strategies=start_strategies)
            payoff_matrix[la][mu] = stats.nash_equilibrium


    cax = plt.imshow(payoff_matrix, alpha=0.9, origin="lower")
    plt.show()


if __name__ == '__main__':
    change_strategy_plot()
