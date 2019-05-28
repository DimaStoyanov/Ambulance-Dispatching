from gt.core.HospitalsModel import *


class NashMixedPlot:
    @staticmethod
    def extract_player_utility(matrix, i):
        return np.array(matrix)[:, :, i]

    @staticmethod
    def mixed_or_pure_solution_value(eqs):
        for eq in eqs:
            if eq[0][0] != 1 and eq[0][1] != 1:
                return int(round(255 * eq[1][1])), 0, int(round(eq[0][1] * 255))
        if len(eqs) == 1:
            eq = eqs[0]
            return int(round(eq[1][1] * 255)), 0, int(round(255 * eq[0][1]))

    @staticmethod
    def is_system_consistent(A, B, eqs):
        for eq in eqs:
            i = 0 if eq[0][0] == 1 else 1
            j = 0 if eq[1][0] == 1 else 1
            if A[i][j] == 0 or B[i][j] == 0:
                return False
        return True

    def find_solution(self, l, mu, n):
        hospital = HospitalsModel(l, mu, n, N_lim, t_c)
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

    def solution_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = []
        points = 10
        x_ticks = [round(x, 2) for x in np.linspace(la_min, la_max, points)]
        y_ticks = [round(x, 2) for x in np.linspace(la_min, la_max, points)]
        for l in x_ticks:
            data.append([])
            for mu in y_ticks:
                data[-1].append(self.find_solution(l, mu, n))
        plt.sca(ax)
        plt.imshow(data, extent=[la_min, la_max, mu_min, mu_max])
        ax.set_title('Nash Mixed Equ N = ' + str(n))
        ax.invert_yaxis()
        ax.set_xticks(np.linspace(la_min, la_max, 10))
        ax.set_xticklabels(x_ticks)
        ax.set_xlabel('Lambda')
        ax.set_ylabel('Mu')
        ax.set_yticks(np.linspace(mu_max, mu_min, 10))
        ax.set_yticklabels(x_ticks)

    def color_bar_2d(self, ax):
        plt.sca(ax)
        data = []
        for r in np.linspace(0, 1, 100):
            data.append([])
            for b in np.linspace(0, 1, 100):
                data[-1].append((r, 0, b))
        plt.imshow(data, extent=[0, 255, 0, 255])
        ax = plt.gca()
        ax.invert_yaxis()
        ax.set_title('Strategies Color Map')
        ax.set_xticks([0, 255])
        ax.set_xticklabels(['A', 'R'])
        ax.set_xlabel('Hospital 1 Strategy')
        ax.set_yticks([0, 255])
        ax.set_yticklabels(['R', 'A'])
        ax.set_ylabel('Hospital 2 Strategy')

    def show(self, filename='../../images/previous/Hospital Mixed Nash Equ'):
        fig = plt.figure(constrained_layout=True, figsize=(25, 25))
        gs = fig.add_gridspec(3, 4)
        self.color_bar_2d(fig.add_subplot(gs[:, 3]))
        self.solution_plot([1, 1], ax=fig.add_subplot(gs[0, 0]))
        self.solution_plot([1, 2], ax=fig.add_subplot(gs[0, 1]))
        self.solution_plot([1, 3], ax=fig.add_subplot(gs[0, 2]))
        self.solution_plot([2, 1], ax=fig.add_subplot(gs[1, 0]))
        self.solution_plot([2, 2], ax=fig.add_subplot(gs[1, 1]))
        self.solution_plot([2, 3], ax=fig.add_subplot(gs[1, 2]))
        self.solution_plot([3, 1], ax=fig.add_subplot(gs[2, 0]))
        self.solution_plot([3, 2], ax=fig.add_subplot(gs[2, 1]))
        self.solution_plot([3, 3], ax=fig.add_subplot(gs[2, 2]))
        fig.savefig(filename)
        plt.show()


if __name__ == '__main__':
    sns.set(style='white')
    NashMixedPlot().show()
