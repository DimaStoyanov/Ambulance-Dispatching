from gt.core.HospitalModel import *


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
    return ', '.join(solution)


def is_system_consistent(A, B, eqs):
    for eq in eqs:
        i = 0 if eq[0][0] == 1 else 1
        j = 0 if eq[1][0] == 1 else 1
        if A[i][j] < 0 or B[i][j] < 0:
            return False
    return True


def find_solution(l, mu, n):
    hospital = HospitalModel(l, mu, n, N_lim, t_c)
    G = hospital.game_matrix()
    A = extract_player_utility(G, 0)
    B = extract_player_utility(G, 1)
    game = nash.Game(A, B)
    eqs = skip_mixed_strategy(game.support_enumeration())
    if is_system_consistent(A, B, eqs):
        return extract_solution(eqs)
    else:
        return 'Inconsistent'


def solution_plot(n, ax=None, legend=False):
    data = {
        'Lambda': [],
        'Mu': [],
        'Nash Equilibrium': []
    }
    for mu in np.linspace(0.5, 3, 100):
        for l in np.linspace(0.5, 3, 100):
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Nash Equilibrium'].append(find_solution(l, mu, n))
    data = pd.DataFrame(data)
    if ax is not None:
        sns.relplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, ax=ax, legend=legend)
        ax.set_title('N = ' + str(n))
    else:
        sns.relplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, legend=legend)


if __name__ == '__main__':
    sns.set(style='white')
    fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(30, 30))
    solution_plot([1, 1], axs[0][0])
    solution_plot([1, 2], axs[0][1])
    solution_plot([1, 3], axs[0][2])
    solution_plot([2, 1], axs[1][0])
    solution_plot([2, 2], axs[1][1])
    solution_plot([2, 3], axs[1][2])
    solution_plot([3, 1], axs[2][0])
    solution_plot([3, 2], axs[2][1])
    solution_plot([3, 3], axs[2][2])
    [plt.close(i) for i in range(2, 11)]
    solution_plot([1, 1], legend='brief')
    fig.savefig('../../images/Hospital Nash Equ')
    plt.savefig('../../images/Hospital Nash Equ(2)')
    plt.show()
