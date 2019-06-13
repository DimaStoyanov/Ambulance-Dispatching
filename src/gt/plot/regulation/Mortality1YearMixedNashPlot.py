from gt.plot.HospitalNashMixedPlot import NashMixedPlot
from gt.core.HospitalWith1YModel import HospitalWith1YM
from common import *


class M1YMixedNashPLot(NashMixedPlot):

    def find_solution(self, l, mu, n):
        hospital = HospitalWith1YM(l, mu, n, N_lim, t_c, cost_transp + cost_op + 1, cost_op + cost_transp)
        G = hospital.game_matrix()
        A = self.extract_player_utility(G, 0)
        B = self.extract_player_utility(G, 1)
        game = nash.Game(A, B)
        eqs = list(game.support_enumeration())
        if self.is_system_consistent(A, B, eqs):
            sol = self.mixed_or_pure_solution_value(eqs)
            return sol
        else:
            return 255, 255, 255


if __name__ == '__main__':
    M1YMixedNashPLot().show('../../../images/regulation/Hospital with M1Y regulation Mixed Nash Equ high revenue')
