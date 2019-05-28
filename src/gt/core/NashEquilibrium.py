from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel


class GameWith3Players:
    def __init__(self, payoff_matrix):
        self.payoff_matrix = payoff_matrix

    def find_pure_nash_equ(self):
        equs = []
        for player1_strategy in range(self.payoff_matrix.shape[0]):
            for player2_strategy in range(self.payoff_matrix.shape[1]):
                for player3_strategy in range(self.payoff_matrix.shape[2]):
                    cur_payoff = self.payoff_matrix[player1_strategy][player2_strategy][player3_strategy]
                    nash_equ = True
                    for indiff_strategies_for_player, player_idx in zip(
                            self.get_indifferent_strategies_payoff_for_each_player(player1_strategy, player2_strategy,
                                                                                   player3_strategy), range(3)):
                        if not self.is_strategy_dominate(cur_payoff, indiff_strategies_for_player, player_idx):
                            nash_equ = False
                    if nash_equ:
                        equs.append((player1_strategy, player2_strategy, player3_strategy))
        return equs

    def get_indifferent_strategies_payoff_for_each_player(self, i, j, k):
        player1_indiff_strategies_payoff = [self.payoff_matrix[x][j][k] for x in range(self.payoff_matrix.shape[0])
                                            if x != i]
        player2_indiff_strategies_payoff = [self.payoff_matrix[i][y][k] for y in
                                            range(self.payoff_matrix.shape[1]) if y != j]
        player3_indiff_strategies_payoff = [self.payoff_matrix[i][j][z] for z in range(self.payoff_matrix.shape[2])
                                            if z != k]

        return player1_indiff_strategies_payoff, player2_indiff_strategies_payoff, player3_indiff_strategies_payoff

    @staticmethod
    def is_strategy_dominate(dominate_strategy_payoff, dominated_strategies_payoff, player_idx):
        for dominated_strategy_payoff in dominated_strategies_payoff:
            if dominate_strategy_payoff[player_idx] < dominated_strategy_payoff[player_idx]:
                return False
        return True

    def find_pne_for_dispatcher_and_hospitals(self):
        equs = self.find_pure_nash_equ()
        return sorted(set([self.convert_strategy_idx_to_name(equ) for equ in equs]))

    def convert_strategy_idx_to_name(self, str_indices):
        disp_strategy = 'N2'
        if str_indices[0] == 1:
            disp_strategy = 'N1'
        elif str_indices[0] == 2:
            return 'BE'

        hosp1_strategy = 'A' if str_indices[1] == 0 else 'R'
        hosp2_strategy = 'A' if str_indices[2] == 0 else 'R'
        return '{}-{}{}'.format(disp_strategy, hosp1_strategy, hosp2_strategy)


if __name__ == '__main__':
    model = DispatcherAndHospitalsModel(2, 2, [2, 2], 5, 10)
    matrix = model.game_matrix(2)
    print(matrix)

    game = GameWith3Players(matrix)
    print(game.find_pne_for_dispatcher_and_hospitals())
