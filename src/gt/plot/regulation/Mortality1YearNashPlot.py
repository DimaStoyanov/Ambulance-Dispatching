from gt.plot.HospitalNashPlot import PureNashPlot
from gt.core.HospitalWith1YModel import HospitalWith1YM
from common import *


class M1YNashPlot(PureNashPlot):
    def find_solution(self, l, mu, n):
        hospital = HospitalWith1YM(l, mu, n, N_lim, t_c, 20, cost_transp + cost_op)
        G = hospital.game_matrix()
        A = self.extract_player_utility(G, 0)
        B = self.extract_player_utility(G, 1)
        game = nash.Game(A, B)
        eqs = self.skip_mixed_strategy(game.support_enumeration())
        if eqs and self.is_system_consistent(eqs, A, B):
            sol = self.extract_solution(eqs)
            return sol
        else:
            return 'Inconsistent'


if __name__ == '__main__':
    M1YNashPlot().show('../../../images/regulation/Hospital with M1Y regulation Nash Equ high revenue')
