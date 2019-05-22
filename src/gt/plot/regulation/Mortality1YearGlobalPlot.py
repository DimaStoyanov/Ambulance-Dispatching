from gt.plot.HospitalGlobalPlot import GlobalEquPlot
from gt.core.HospitalWith1YModel import HospitalWith1YM
from common import *


class M1YGlobalPlot(GlobalEquPlot):
    def __init__(self):
        self.op = np.max

    def global_matrix(self, la, mu, n):
        model = HospitalWith1YM(la, mu, n, N_lim, 1, 13, 13)
        return model.global_matrix()

    def append_if_consistent(self, data, la, strategy, val):
        if abs(val) < 1e8:
            data['Lambda'].append(la)
            data['Strategy'].append(strategy)
            data['Proportion of cured patients'].append(val)

    def line_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = {
            'Lambda': [],
            'Strategy': [],
            'Proportion of cured patients': []
        }
        mu = 2
        for la in np.linspace(0.05, 5, 30):
            global_matrix = HospitalWith1YM(la, mu, n, N_lim, t_c, 13, 13).global_matrix()

            self.append_if_consistent(data, la, 'AA', global_matrix[0][0])
            self.append_if_consistent(data, la, 'AR', global_matrix[0][1])
            self.append_if_consistent(data, la, 'RA', global_matrix[1][0])
            self.append_if_consistent(data, la, 'RR', global_matrix[1][1])

        data = pd.DataFrame(data)
        ax = sns.lineplot(x='Lambda', y='Proportion of cured patients', hue='Strategy', data=data, ax=ax)
        if ax is not None:
            ax.set_title('N = ' + str(n))
        # [ax.lines[i].set_linestyle("--") for i in [0, 2]]

    def line_plot_cascade(self):
        fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(35, 35))
        for n1 in range(5):
            for n2 in range(5):
                self.line_plot([n1 + 1, n2 + 1], axs[n1][n2])
        plt.savefig('../../../images/regulation/Hospital with M1Y regulation cured rate')
        plt.show()


if __name__ == '__main__':
    M1YGlobalPlot().show('../../../images/regulation/Hospital with M1Y regulation Global Equ')
    M1YGlobalPlot().line_plot_cascade()
