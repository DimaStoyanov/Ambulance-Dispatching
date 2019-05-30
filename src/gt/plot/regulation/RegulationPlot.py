from common import *
from gt.core.HospitalWithD2BModel import HospitalWithD2BModel
from gt.core.HospitalWith1YModel import HospitalWith1YM
from gt.plot.HospitalNashPlot import PureNashPlot
from gt.core.HospitalsModel import HospitalsModel

points = 10


class RegulationPlot(PureNashPlot):

    def strategies_intersects(self, global_strategies, nash_strategies):
        return any(filter(lambda s: s in nash_strategies, global_strategies))

    @staticmethod
    def global_solution(g):
        solution = np.max(g)
        if abs(solution) == 0:
            return 'Inconsistent'
        equs = []
        if g[0][0] == solution:
            equs.append('AA')
        elif g[0][1] == solution:
            equs.append('AR')
        elif g[1][0] == solution:
            equs.append('RA')
        else:
            equs.append('RR')
        return ','.join(equs)

    def find_nash(self, g):
        A = self.extract_player_utility(g, 0)
        B = self.extract_player_utility(g, 1)
        game = nash.Game(A, B)

        eqs = self.skip_mixed_strategy(game.support_enumeration())
        if eqs and self.is_system_consistent(eqs, A, B):
            return self.extract_solution(eqs)
        else:
            return 'Inconsistent'

    def d2b_nash_optima(self, n, revenue):
        matches = 0
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                model = HospitalWithD2BModel(la, mu, n, N_lim, t_c, revenue, cost_transp, cost_op)
                nash_equs = self.find_nash(model.game_matrix())
                global_equs = self.global_solution(model.global_matrix())
                if self.strategies_intersects(global_equs, nash_equs):
                    matches += 1
        return matches / points / points

    def m1y_nash_optima(self, n, revenue):
        matches = 0
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                model = HospitalWith1YM(la, mu, n, N_lim, t_c, revenue, cost_transp + cost_op)
                nash_equs = self.find_nash(model.game_matrix())
                global_equs = self.global_solution(model.global_matrix())
                if self.strategies_intersects(global_equs, nash_equs):
                    matches += 1
        return matches / points / points

    def base_model_nash_optima(self, n):
        matches = 0
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                model = HospitalsModel(la, mu, n, N_lim, t_c)
                nash_equs = self.find_nash(model.game_matrix())
                global_equs = self.global_solution(model.global_average_time_matrix())
                if self.strategies_intersects(global_equs, nash_equs):
                    matches += 1
        return matches / points / points

    def diff_between_optima_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = {
            'Revenue': [cost_op + cost_transp] * 2 + [cost_transp] * 2 + [-150, 150],
            'Regulation': ['Transportation and surgery cost'] * 2 + ['Transportation cost'] * 2 + ['No regulation'] * 2,
            'Nash Equ proximity to global Equ': [0, 1] * 2 + [self.base_model_nash_optima(n)] * 2
        }
        for revenue in np.linspace(-150, 150, 20):
            data['Revenue'].append(revenue)
            data['Regulation'].append('Door-to-balloon time')
            data['Nash Equ proximity to global Equ'].append(self.d2b_nash_optima(n, revenue))

            data['Revenue'].append(revenue)
            data['Regulation'].append('1 Year Mortality')
            data['Nash Equ proximity to global Equ'].append(self.m1y_nash_optima(n, revenue))

        data = pd.DataFrame(data)
        sns.lineplot(x='Revenue', y='Nash Equ proximity to global Equ', hue='Regulation', data=data, ax=ax)
        ax.legend(loc='lower right')
        [ax.lines[i].set_linestyle("--") for i in [3, 4]]

        if ax is not None:
            ax.set_title('N = {}'.format(n))

    def regulation_plot_cascade(self):
        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
        for n1 in range(3):
            for n2 in range(3):
                self.diff_between_optima_plot([n1 + 1, n2 + 1], axs[n1][n2])
        plt.savefig('../../../images/regulation/Regulation comparision')
        plt.show()


if __name__ == '__main__':
    RegulationPlot().regulation_plot_cascade()
