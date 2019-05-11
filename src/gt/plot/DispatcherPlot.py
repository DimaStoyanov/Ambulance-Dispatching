from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
from neng.game import Game
from common import *


def find_nash(la, mu, n, print_matrix=False):
    model = DispatcherAndHospitalsModel(la, mu, n, 3, 10)
    matrix = model.game_matrix()
    if print_matrix:
        print(matrix)

    text = "NFG 1 R \"Ambulance Dispatching Game\" { \"Dispatcher\" \"Hospital1\" \"Hospital2\" }\n\n"
    text += "{ { \"N2\" \"N1\" \"BE\" }\n"
    text += "{ \"A\" \"R\" }\n"
    text += "{ \"A\" \"R\" }\n"
    text += "}\n\"\"\n\n"

    text += "{\n"
    for k in range(2):
        for j in range(2):
            for i in range(3):
                text += "{ \"\" %f, %f, %f }\n" % (matrix[i][j][k][0], matrix[i][j][k][2], matrix[i][j][k][2])
    text += "}\n"
    text += "1 2 3 4 5 6 7 8 9 10 11 12"

    game = Game(text)
    sol = game.findEquilibria('pne')
    return extract_strategies_from_solutions(sol, matrix)


def extract_strategies_from_solutions(solutions, payoff_matrix):
    strategies = set()
    if not solutions:
        return strategies
    for sol in solutions:
        cur_stra = ''
        if sol[0][0] == 1:
            cur_stra += 'N2'
        elif sol[0][1] == 1:
            cur_stra += 'N1'
        else:
            cur_stra += 'BE'
            strategies.add(cur_stra)
            continue

        cur_stra += ';'
        if sol[1][0] == 1:
            cur_stra += 'A'
        else:
            cur_stra += 'R'

        if sol[2][0] == 1:
            cur_stra += 'A'
        else:
            cur_stra += 'R'
        strategies.add(cur_stra)
    if is_inconsistent(strategies, payoff_matrix):
        return ['Inconsistent']
    return strategies


def is_inconsistent(strategies, payoff):
    for strategy in strategies:
        if strategy == 'BE':
            if payoff[2][0][0][1] < 0 or payoff[2][0][0][2] < 0:
                return True
            continue
        cur = payoff[0] if strategy[:2] == 'N2' else payoff[1]
        cur = cur[0] if strategy[3] == 'A' else cur[1]
        cur = cur[0] if strategy[4] == 'A' else cur[1]
        if cur[1] < 0 or cur[2] < 0:
            return True


def solution_plot(n, ax=None, legend=False):
    print('Computing for n = {}'.format(n))
    data = {
        'Lambda': [],
        'Mu': [],
        'Nash Equilibrium': []
    }
    for mu in np.linspace(0.5, 3, 30):
        # print('Computing for mu={}'.format(mu))
        for l in np.linspace(0.5, 3, 30):
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Nash Equilibrium'].append(','.join(find_nash(l, mu, n)))
    data = pd.DataFrame(data)
    if ax is not None:
        sns.scatterplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, ax=ax, legend=legend, marker='s', s=1000)
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
