from common import *
from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
import nashpy as nash


def disp_strategy_idx(disp_strategy):
    if disp_strategy == 'N2':
        return 0
    return 1 if disp_strategy == 'N1' else 2


def extract_player_utility(matrix, i):
    return np.array(matrix)[:, :, i]


def skip_mixed_strategy(eqs):
    return list(filter(lambda x: x[0][0] == 0 or x[0][0] == 1, eqs))


def extract_solution(eqs):
    solution = set()
    for eq in eqs:
        cur = 'A' if eq[0][0] == 1 else 'R'
        cur += 'A' if eq[1][0] == 1 else 'R'
        solution.add(cur)
    return solution


def is_system_consistent(eqs, A, B):
    for eq in eqs:
        i = 0 if eq[0][0] == 1 else 1
        j = 0 if eq[1][0] == 1 else 1
        if abs(A[i][j]) == 0 or abs(B[i][j]) ==  0:
            return False
    return True


def find_nash(full_matrix, disp_strategy_idx):
    matrix = full_matrix[disp_strategy_idx, :, :, 1:]
    A = extract_player_utility(matrix, 0)
    B = extract_player_utility(matrix, 1)

    game = nash.Game(A, B)
    equs = skip_mixed_strategy(game.support_enumeration())
    if equs and is_system_consistent(equs, A, B):
        sol = extract_solution(equs)
        return sol
    else:
        return 'Inconsistent'


def find_global(full_matrix, disp_strategy_idx):
    g = full_matrix[disp_strategy_idx]
    solution = np.min(g)
    if abs(solution) >= 1e8:
        return 'Inconsistent'
    equs = []
    if g[0][0] == solution:
        equs.append('AA')
    elif g[0][1] == solution:
        equs.append('AR')
    elif g[1][0] == solution:
        equs.append('RA')
    else:
        equs.append('RR')
    return equs


def intersection(a, b):
    res = []
    for x, y in zip(a, b):
        res.append(any(i in y for i in x))
    return res


def disp_regulation(n):
    points = 10
    matches = np.array([0] * 3)
    for la in np.linspace(0.05, 5, points):
        for mu in np.linspace(0.05, 5, points):
            model = DispatcherAndHospitalsModel(la, mu, n, N_lim, t_c)
            game_matrix = model.game_matrix()
            global_matrix = model.global_average_time_matrix()
            nash_equs = [find_nash(game_matrix, i) for i in range(3)]
            global_equs = [find_global(global_matrix, i) for i in range(3)]
            matches += intersection(nash_equs, global_equs)
    return matches / ([points ** 2] * 3)


def disp_regulation_plot(n, ax=None):
    print('Computing for n = {}'.format(n))
    data = pd.DataFrame({
        'Dispatcher': ['Nearest 2', 'Nearest 1', 'Best Expectation'],
        'Proximity to global solution': disp_regulation(n)
    })
    sns.barplot(x='Dispatcher', y='Proximity to global solution', data=data, ax=ax)
    ax.set_title('N = {}'.format(n))


def show():
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
    for n1 in range(3):
        for n2 in range(3):
            disp_regulation_plot([n1 + 1, n2 + 1], axs[n1][n2])
    plt.savefig('../../../images/regulation/Dispatcher regulation')
    plt.show()


if __name__ == '__main__':
    show()
