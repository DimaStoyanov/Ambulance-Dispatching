from gt.core.HospitalsModel import *


def extract_player_utility(matrix, i):
    return np.array(matrix)[:, :, i]


def mixed_or_pure_solution_value(eqs):
    for eq in eqs:
        if eq[0][0] != 1 and eq[0][1] != 1:
            return -1 + eq[0][1] + eq[1][1]
    if len(eqs) == 1:
        eq = eqs[0]
        return -1 + eq[0][1] + eq[1][1]


def is_system_consistent(A, B, eqs):
    for eq in eqs:
        i = 0 if eq[0][0] == 1 else 1
        j = 0 if eq[1][0] == 1 else 1
        if A[i][j] < 0 or B[i][j] < 0:
            return False
    return True


def find_solution(l, mu, n):
    hospital = HospitalsModel(l, mu, n, N_lim, t_c)
    G = hospital.game_matrix()
    A = extract_player_utility(G, 0)
    B = extract_player_utility(G, 1)
    game = nash.Game(A, B)
    eqs = list(game.support_enumeration())
    if is_system_consistent(A, B, eqs):
        sol = mixed_or_pure_solution_value(eqs)
        return sol
    else:
        return None


def solution_plot(n, ax=None):
    print('Computing for n = {}'.format(n))
    data = {
        'Lambda': [],
        'Mu': [],
        'Nash Equilibrium': []
    }
    x_ticks = [round(x, 2) for x in np.linspace(0.01, 5, 10)]
    y_ticks = [round(x, 2) for x in np.linspace(0.01, 5, 10)]
    for mu in y_ticks:
        for l in x_ticks:
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Nash Equilibrium'].append(find_solution(l, mu, n))
    data = pd.DataFrame(data).pivot('Mu', 'Lambda',  'Nash Equilibrium')
    sns.heatmap(data, ax=ax, vmin=-1, vmax=1, cmap='coolwarm')
    ax.set_title('N = ' + str(n))
    ax.invert_yaxis()
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(['AA', 'AR/RA', 'RR'])


if __name__ == '__main__':
    sns.set(style='white')
    fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(17, 17))
    solution_plot([1, 1], axs[0][0])
    solution_plot([1, 2], axs[0][1])
    solution_plot([1, 3], axs[0][2])
    solution_plot([2, 1], axs[1][0])
    solution_plot([2, 2], axs[1][1])
    solution_plot([2, 3], axs[1][2])
    solution_plot([3, 1], axs[2][0])
    solution_plot([3, 2], axs[2][1])
    solution_plot([3, 3], axs[2][2])
    fig.savefig('../../images/previous/Hospital Mixed Nash Equ')
    plt.show()
