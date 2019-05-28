from gt.plot.HospitalNashPlot import PureNashPlot
from gt.core.HospitalWith1YModel import HospitalWith1YM
from common import *

class M1YNashPlot(PureNashPlot):
    def find_solution(self, l, mu, n):
        hospital = HospitalWith1YM(l, mu, n, N_lim, t_c, 5, cost_transp + cost_op)
        G = hospital.game_matrix()
        A = self.extract_player_utility(G, 0)
        B = self.extract_player_utility(G, 1)
        game = nash.Game(A, B)
        eqs = list(game.support_enumeration())
        if self.is_system_consistent(A, B, eqs):
            sol = self.skip_mixed_strategy(eqs)
            return sol
        else:
            return None


if __name__ == '__main__':
    M1YNashPlot().show('../../../images/regulation/Hospital with M1Y regulation Mixed Nash Equ low revenue')
