from common import *
from simulation.stats.ChangeStrategyEquilibriumStats import ChangeStrategyEquilibriumStats
from matplotlib import colors

payoff_to_num = {
    'AAA': 0, 'ARA': 1,
    'AAR': 2, 'ARR': 3,
    'RAA': 4, 'RRA': 5,
    'RAR': 6, 'RRR': 7,
}


def change_strategy_plot(start_strategies='AAA', points=8):
    payoff_matrix = {
        "Lambda": [],
        "Mu": [],
        "Payoff": []
    }
    for la, i in zip(list(reversed(np.linspace(12, 14, points))), range(points)):
        for mu, j in zip(np.linspace(120, 124, points), range(points)):
            stats = ChangeStrategyEquilibriumStats(la, mu, start_strategies=start_strategies)
            payoff_matrix['Lambda'].append(round(la, 2))
            payoff_matrix['Mu'].append(round(mu, 2))
            payoff_matrix['Payoff'].append(",".join(stats.nash_equilibrium))

    fig = plt.figure()
    fig.set_size_inches(16, 16)
    ax = sns.scatterplot(data=payoff_matrix, x='Lambda', y='Mu', hue='Payoff', s=200_000 / points, marker='s')
    plt.title(
        "Nash Equilibrium for different crowding level in system (starting from {} strategy)".format(start_strategies),
        fontsize=26)
    plt.xlabel("Patient's incoming rate", fontsize=26)
    plt.ylabel("Patient's serving rate", fontsize=26)
    plt.savefig('../../images/Nash Equ from ' + start_strategies)
    plt.show()

    print(payoff_matrix)


if __name__ == '__main__':
    change_strategy_plot()
    change_strategy_plot('RRR')
