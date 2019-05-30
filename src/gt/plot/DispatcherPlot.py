from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
from gt.core.NashEquilibrium import GameWith3Players
from common import *


def find_nash(la, mu, n, print_matrix=False):
    model = DispatcherAndHospitalsModel(la, mu, n, N_lim, t_c)
    matrix = model.game_matrix()
    if print_matrix:
        print(matrix)

    game = GameWith3Players(matrix)
    equs = game.find_pne_for_dispatcher_and_hospitals()
    if is_inconsistent(equs, matrix):
        return ['Inconsistent']
    return equs


def is_inconsistent(strategies, payoff):
    for strategy in strategies:
        if strategy[:2] == 'BE':
            if payoff[2][0][0][1] == 0 or payoff[2][0][0][2] == 0:
                return True
            continue
        cur = payoff[0] if strategy[:2] == 'N2' else payoff[1]
        cur = cur[0] if strategy[3] == 'A' else cur[1]
        cur = cur[0] if strategy[4] == 'A' else cur[1]
        if cur[1] == 0 or cur[2] == 0:
            return True


def solution_plot(n, ax=None, legend=False):
    print('Computing for n = {}'.format(n))
    data = {
        'Lambda': [],
        'Mu': [],
        'Nash Equilibrium': []
    }
    for mu in np.linspace(mu_min, mu_max, 30):
        # print('Computing for mu={}'.format(mu))
        for l in np.linspace(la_min, la_max, 30):
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Nash Equilibrium'].append(','.join(find_nash(l, mu, n)))
    data = pd.DataFrame(data)
    if ax is not None:
        sns.scatterplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, ax=ax, legend=legend, marker='s', s=1000,
                        palette=disp_palette)
        ax.set_title('N = ' + str(n))
    else:
        sns.scatterplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, legend=legend, marker='s', s=1000)


if __name__ == '__main__':
    _, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
    solution_plot([1, 1], ax=axs[0][0], legend='brief')
    solution_plot([1, 2], ax=axs[0][1], legend='brief')
    solution_plot([1, 3], ax=axs[0][2], legend='brief')
    solution_plot([2, 1], ax=axs[1][0], legend='brief')
    solution_plot([2, 2], ax=axs[1][1], legend='brief')
    solution_plot([2, 3], ax=axs[1][2], legend='brief')
    solution_plot([3, 1], ax=axs[2][0], legend='brief')
    solution_plot([3, 2], ax=axs[2][1], legend='brief')
    solution_plot([3, 3], ax=axs[2][2], legend='brief')
    plt.savefig('../../images/Dispatcher/Dispatcher Nash Equilibrium')
    plt.show()
