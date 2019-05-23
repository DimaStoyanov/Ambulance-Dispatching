from gt.plot.HospitalNashPlot import PureNashPlot
from common import *
from gt.core.HospitalWithD2BModel import HospitalWithD2BModel


class D2BPureNashPlot(PureNashPlot):

    def find_solution(self, l, mu, n):
        hospital = HospitalWithD2BModel(l, mu, n, N_lim, t_c, 20, 3, 10)
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
    sns.set(style='white')
    D2BPureNashPlot().show('../../../images/regulation/Hospital with D2B regulation Nash Equ')
