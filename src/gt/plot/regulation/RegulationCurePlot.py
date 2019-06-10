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

    def extract_rate_for_solutions(self, eqs, global_matrix):
        rates = []
        for eq in eqs:
            i = 0 if eq[0][0] == 1 else 1
            j = 0 if eq[1][0] == 1 else 1
            rates.append(global_matrix[i][j])
        return np.average(rates)

    def find_nash(self, g):
        A = self.extract_player_utility(g, 0)
        B = self.extract_player_utility(g, 1)
        game = nash.Game(A, B)

        eqs = self.skip_mixed_strategy(game.support_enumeration())
        if eqs and self.is_system_consistent(eqs, A, B):
            return eqs
        else:
            return []

    def find_rate(self, g, rates_matrix):
        return self.extract_rate_for_solutions(self.find_nash(g), rates_matrix)

    def d2b_nash_optima(self, n, revenue):
        rates = []
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                model = HospitalWithD2BModel(la, mu, n, N_lim, t_c, revenue, cost_transp, cost_op)
                global_matrix = model.global_matrix()
                rates.append(self.find_rate(model.game_matrix(), global_matrix))
        return np.average(np.nan_to_num(rates))

    def m1y_nash_optima(self, n, revenue):
        rates = []
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                model = HospitalWith1YM(la, mu, n, N_lim, t_c, revenue, cost_transp + cost_op)
                rates.append(self.find_rate(model.game_matrix(), model.global_matrix()))
        return np.average(np.nan_to_num(rates))

    def find_base_rate(self, la, mu, n):
        base_model = HospitalsModel(la, mu, n, N_lim, t_c)
        equs = self.find_nash(base_model.game_matrix())
        lambdas, times = base_model.lambdas_and_times()
        rates = []
        for eq in equs:
            i = 0 if eq[0][0] == 1 else 1
            j = 0 if eq[1][0] == 1 else 1
            p_mort = HospitalWith1YM(la, mu, n, N_lim, t_c, revenue, cost_op + cost_transp).p_mortality(times[i][j])
            rates.append((1 - p_mort))

        return np.average(np.nan_to_num(rates))

    def base_model_nash_optima(self, n):
        rates = []
        for la in np.linspace(la_min, la_max, points):
            for mu in np.linspace(mu_min, mu_max, points):
                rates.append(self.find_base_rate(la, mu, n))
        return np.average(np.nan_to_num(rates))

    def diff_between_optima_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        base_rate = self.base_model_nash_optima(n)
        data = {
            'Revenue': [cost_op + cost_transp] * 2 + [cost_transp] * 2 + [-30, 150],
            'Regulation': ['Transportation and surgery cost'] * 2 + ['Transportation cost'] * 2 + ['No regulation'] * 2,
            'Cured rate': [base_rate - 0.05, base_rate + 0.05] * 2 + [base_rate] * 2
        }
        for revenue in np.linspace(-30, 150, 20):
            data['Revenue'].append(revenue)
            data['Regulation'].append('Door-to-balloon time')
            data['Cured rate'].append(self.d2b_nash_optima(n, revenue))

            data['Revenue'].append(revenue)
            data['Regulation'].append('1 Year Mortality')
            data['Cured rate'].append(self.m1y_nash_optima(n, revenue))

        data = pd.DataFrame(data)
        sns.lineplot(x='Revenue', y='Cured rate', hue='Regulation', data=data, ax=ax)
        ax.legend(loc='upper left')
        [ax.lines[i].set_linestyle("--") for i in [3, 4]]

        if ax is not None:
            ax.set_title('N = {}'.format(n))

    def regulation_plot_cascade(self):
        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
        for n1 in range(3):
            for n2 in range(3):
                self.diff_between_optima_plot([n1 + 1, n2 + 1], axs[n1][n2])
        plt.savefig('../../../images/regulation/Regulation comparision by cure rate')
        plt.show()


if __name__ == '__main__':
    RegulationPlot().regulation_plot_cascade()
