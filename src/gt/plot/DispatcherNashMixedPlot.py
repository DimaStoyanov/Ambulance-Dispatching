from common import *
from gt.core.HospitalsAndDispatcherModel import DispatcherAndHospitalsModel
from gt.plot.HospitalNashMixedPlot import *


class DispatcherMixedNashPlot(NashMixedPlot):
    def find_solution(self, l, mu, n, disp_strategy_index):
        hospital = DispatcherAndHospitalsModel(l, mu, n, N_lim, t_c)
        G = hospital.game_matrix()[disp_strategy_index]
        A = self.extract_player_utility(G, 1)
        B = self.extract_player_utility(G, 2)
        game = nash.Game(A, B)
        eqs = list(game.support_enumeration())
        if self.is_system_consistent(A, B, eqs):
            sol = self.mixed_or_pure_solution_value(eqs)
            return sol
        else:
            return 255, 255, 255

    def solution_plot(self, n, disp_strategy_idx, ax=None):
        print('Computing for n = {}'.format(n))
        data = []
        points = 20
        x_ticks = [round(x, 2) for x in np.linspace(la_min, la_max, points)]
        y_ticks = [round(x, 2) for x in np.linspace(la_min, la_max, points)]
        for l in x_ticks:
            data.append([])
            for mu in y_ticks:
                data[-1].append(self.find_solution(l, mu, n, disp_strategy_idx))
        plt.sca(ax)
        plt.imshow(data, extent=[la_min, la_max, mu_min, mu_max])
        ax.set_title('Nash Mixed Equ N = ' + str(n), fontdict={'fontsize': 20})
        ax.invert_yaxis()
        ax.set_xticks(np.linspace(la_min, la_max, 10))
        ax.set_xticklabels(x_ticks, fontdict={'fontsize': 14})
        ax.set_xlabel('Lambda', fontdict={'fontsize': 18})
        ax.set_ylabel('Mu', fontdict={'fontsize': 18})
        ax.set_yticks(np.linspace(mu_max, mu_min, 10))
        ax.set_yticklabels(x_ticks, fontdict={'fontsize': 14})

    def show(self, disp_strategy_idx, filename='../../images/previous/Hospital Mixed Nash Equ'):
        fig = plt.figure(constrained_layout=True, figsize=(24, 24))
        gs = fig.add_gridspec(3, 4)
        self.color_bar_2d(fig.add_subplot(gs[:, 3]))
        self.solution_plot([1, 1], disp_strategy_idx, ax=fig.add_subplot(gs[0, 0]))
        self.solution_plot([1, 2], disp_strategy_idx, ax=fig.add_subplot(gs[0, 1]))
        self.solution_plot([1, 3], disp_strategy_idx, ax=fig.add_subplot(gs[0, 2]))
        self.solution_plot([2, 1], disp_strategy_idx, ax=fig.add_subplot(gs[1, 0]))
        self.solution_plot([2, 2], disp_strategy_idx, ax=fig.add_subplot(gs[1, 1]))
        self.solution_plot([2, 3], disp_strategy_idx, ax=fig.add_subplot(gs[1, 2]))
        self.solution_plot([3, 1], disp_strategy_idx, ax=fig.add_subplot(gs[2, 0]))
        self.solution_plot([3, 2], disp_strategy_idx, ax=fig.add_subplot(gs[2, 1]))
        self.solution_plot([3, 3], disp_strategy_idx, ax=fig.add_subplot(gs[2, 2]))
        fig.savefig(filename)
        plt.show()


if __name__ == '__main__':
    plot = DispatcherMixedNashPlot()
    plot.show(0, '../../images/dispatcher/Hospital Mixed Nash Equ for Dispatcher N2')
    plot.show(1, '../../images/dispatcher/Hospital Mixed Nash Equ for Dispatcher N1')
