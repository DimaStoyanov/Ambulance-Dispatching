from gt.plot.HospitalNashMixedPlot import NashMixedPlot
from gt.core.HospitalWithD2BModel import HospitalWithD2BModel
from common import *


class D2BNashMixedPlot(NashMixedPlot):

    def find_solution(self, l, mu, n):
        hospital = HospitalWithD2BModel(l, mu, n, N_lim, t_c, 13, 3, 10)
        G = hospital.game_matrix()
        A = self.extract_player_utility(G, 0)
        B = self.extract_player_utility(G, 1)
        game = nash.Game(A, B)
        eqs = list(game.support_enumeration())
        if self.is_system_consistent(A, B, eqs):
            sol = self.mixed_or_pure_solution_value(eqs)
            return sol
        else:
            return None


if __name__ == '__main__':
    D2BNashMixedPlot().show('../../../images/regulation/Hospital with D2B regulation Mixed Nash Equ')
