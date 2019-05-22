from gt.plot.HospitalNashMixedPlot import *
from gt.core.HospitalWith1YModel import HospitalWith1YM


def find_solution(l, mu, n):
    hospital = HospitalWith1YM(l, mu, n, N_lim, t_c, 30, 13)
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
    fig.savefig('../../../images/regulation/Hospital with 1YM regulation Mixed Nash Equ')
    plt.show()
