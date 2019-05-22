from gt.core.HospitalsModel import *


class GlobalEquPlot:

    def global_matrix(self, la, mu, n):
        hospital = HospitalsModel(la, mu, n, N_lim, t_c)
        return hospital.global_average_time_matrix()

    def global_solution(self, la, mu, n):
        g = self.global_matrix(la, mu, n)
        solution = np.min(g)
        if abs(solution) >= 1e8:
            return 'Inconsistent'
        if g[0][0] == solution:
            return 'AA'
        elif g[0][1] == solution:
            return 'AR'
        elif g[1][0] == solution:
            return 'RA'
        else:
            return 'RR'

    def global_solution_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = {
            'Lambda': [],
            'Mu': [],
            'Optimal Strategy': []
        }
        for l in np.linspace(0.01, 3, 30):
            for mu in np.linspace(0.01, 3, 30):
                data['Lambda'].append(l)
                data['Mu'].append(mu)
                data['Optimal Strategy'].append(self.global_solution(l, mu, n))
        data = pd.DataFrame(data)
        sns.scatterplot(x='Lambda', y='Mu', hue='Optimal Strategy', data=data, ax=ax, marker='s', s=1000)
        if ax is not None:
            ax.set_title('N = ' + str(n))

    def show(self, filename='../../images/previous/Global Nash Equ'):
        sns.set(style='ticks')
        fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(15, 15))
        self.global_solution_plot([1, 1], axs[0][0])
        self.global_solution_plot([1, 2], axs[0][1])
        self.global_solution_plot([1, 3], axs[0][2])
        self.global_solution_plot([2, 1], axs[1][0])
        self.global_solution_plot([2, 2], axs[1][1])
        self.global_solution_plot([2, 3], axs[1][2])
        self.global_solution_plot([3, 1], axs[2][0])
        self.global_solution_plot([3, 2], axs[2][1])
        self.global_solution_plot([3, 3], axs[2][2])
        fig.savefig(filename)
        plt.show()


if __name__ == '__main__':
    GlobalEquPlot().show()
