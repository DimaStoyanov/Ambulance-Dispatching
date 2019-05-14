from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
from neng.game import Game
from gt.plot.HospitalNashMixedPlot import *
from common import *


def find_solution(l, mu, n, disp_strategy_index):
    hospital = DispatcherAndHospitalsModel(l, mu, n, N_lim, t_c)
    G = hospital.game_matrix()[disp_strategy_index]
    A = extract_player_utility(G, 1)
    B = extract_player_utility(G, 2)
    game = nash.Game(A, B)
    eqs = list(game.support_enumeration())
    if is_system_consistent(A, B, eqs):
        sol = mixed_or_pure_solution_value(eqs)
        return sol
    else:
        return None


def solution_plot(disp_strategy, n, ax=None):
    disp_strategy_idx = 0 if disp_strategy == 'N2' else 1
    print('Computing for n = {}'.format(n))
    data = {
        'Lambda': [],
        'Mu': [],
        'Nash Equilibrium': []
    }
    x_ticks = [round(x, 2) for x in np.linspace(0.01, 10, 20)]
    y_ticks = [round(x, 2) for x in np.linspace(0.01, 10, 20)]
    for mu in y_ticks:
        for l in x_ticks:
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Nash Equilibrium'].append(find_solution(l, mu, n, disp_strategy_idx))
    data = pd.DataFrame(data).pivot( 'Mu', 'Lambda', 'Nash Equilibrium')
    sns.heatmap(data, ax=ax, vmin=-1, vmax=1, cmap='coolwarm')
    ax.set_title('Dispatcher Strategy: {}, N = {}'.format(disp_strategy, n))
    ax.invert_yaxis()
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(['AA', 'AR/RA', 'RR'])


def mixed_plot(dispatcher_strategy):
    fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(20, 20))
    solution_plot(dispatcher_strategy, [1, 1], axs[0][0])
    solution_plot(dispatcher_strategy, [1, 2], axs[0][1])
    solution_plot(dispatcher_strategy, [1, 3], axs[0][2])
    solution_plot(dispatcher_strategy, [2, 1], axs[1][0])
    solution_plot(dispatcher_strategy, [2, 2], axs[1][1])
    solution_plot(dispatcher_strategy, [2, 3], axs[1][2])
    solution_plot(dispatcher_strategy, [3, 1], axs[2][0])
    solution_plot(dispatcher_strategy, [3, 2], axs[2][1])
    solution_plot(dispatcher_strategy, [3, 3], axs[2][2])
    fig.savefig('../../images/dispatcher/Hospital Mixed Nash Equ for Dispatcher {}'.format(dispatcher_strategy))
    plt.show()


if __name__ == '__main__':
    sns.set(style='white')
    mixed_plot('N2')
    mixed_plot('N1')
