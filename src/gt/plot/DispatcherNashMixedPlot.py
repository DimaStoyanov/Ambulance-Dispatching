from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
from neng.game import Game
from common import *


def find_solution(l, mu, n):
    hospital = DispatcherAndHospitalsModel(l, mu, n, N_lim, t_c)
    G = hospital.game_matrix()
    A = extract_player_utility(G, 0)
    B = extract_player_utility(G, 1)
    game = nash.Game(A, B)
    eqs = list(game.support_enumeration())
    if is_system_consistent(A, B, eqs):
        sol = mixed_solution_value(eqs)
        return sol
    else:
        return None
