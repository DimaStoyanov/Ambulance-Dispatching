from gt.core.HospitalsModel import *


class PureNashPlot:

    @staticmethod
    def extract_player_utility(matrix, i):
        return np.array(matrix)[:, :, i]

    @staticmethod
    def skip_mixed_strategy(eqs):
        return list(filter(lambda x: x[0][0] == 0 or x[0][0] == 1, eqs))

    @staticmethod
    def extract_solution(eqs):
        solution = set()
        for eq in eqs:
            cur = 'A' if eq[0][0] == 1 else 'R'
            cur += 'A' if eq[1][0] == 1 else 'R'
            solution.add(cur)
        return ', '.join(solution)

    @staticmethod
    def is_system_consistent(eqs, A, B):
        for eq in eqs:
            i = 0 if eq[0][0] == 1 else 1
            j = 0 if eq[1][0] == 1 else 1
            if abs(A[i][j]) > 1e8 or abs(B[i][j]) > 1e8:
                return False
        return True

    def find_solution(self, l, mu, n):
        hospital = HospitalsModel(l, mu, n, N_lim, t_c)
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

    def solution_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = {
            'Lambda': [],
            'Mu': [],
            'Nash Equilibrium': []
        }
        for mu in np.linspace(0.01, 3, 30):
            for l in np.linspace(0.01, 3, 30):
                data['Lambda'].append(l)
                data['Mu'].append(mu)
                data['Nash Equilibrium'].append(self.find_solution(l, mu, n))
        data = pd.DataFrame(data)
        if ax is not None:
            sns.scatterplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, ax=ax, marker='s', s=1000)
            ax.set_title('N = ' + str(n))
        else:
            sns.relplot(x='Lambda', y='Mu', hue='Nash Equilibrium', data=data, marker='s', s=1000)

    def show(self, filename='../../images/previous/Hospital Nash Equ'):
        fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(15, 15))
        self.solution_plot([1, 1], axs[0][0])
        self.solution_plot([1, 2], axs[0][1])
        self.solution_plot([1, 3], axs[0][2])
        self.solution_plot([2, 1], axs[1][0])
        self.solution_plot([2, 2], axs[1][1])
        self.solution_plot([2, 3], axs[1][2])
        self.solution_plot([3, 1], axs[2][0])
        self.solution_plot([3, 2], axs[2][1])
        self.solution_plot([3, 3], axs[2][2])
        fig.savefig(filename)
        plt.show()


if __name__ == '__main__':
    sns.set(style='white')
    PureNashPlot().show()
