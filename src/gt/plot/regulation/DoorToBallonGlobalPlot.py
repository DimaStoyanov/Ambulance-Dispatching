from gt.plot.HospitalGlobalPlot import GlobalEquPlot
from gt.core.HospitalWithD2BModel import HospitalWithD2BModel
from common import *


class D2BGlobalPlot(GlobalEquPlot):
    def global_matrix(self, la, mu, n):
        model = HospitalWithD2BModel(la, mu, n, N_lim, 1, 13, 3, 10)
        return model.global_matrix()

    def append_if_consistent(self, data, la, strategy, val):
        if abs(val) < 1e8:
            data['Lambda'].append(la)
            data['Strategy'].append(strategy)
            data['Proportion of cured patients'].append(val)

    def lin_plot(self, n, ax=None):
        print('Computing for n = {}'.format(n))
        data = {
            'Lambda': [],
            'Strategy': [],
            'Proportion of cured patients': []
        }
        mu = 1
        for la in np.linspace(0.01, 5, 30):
            global_matrix = HospitalWithD2BModel(la, mu, n, N_lim, t_c, 13, 3, 10).global_matrix()

            self.append_if_consistent(data, la, 'AA', global_matrix[0][0])
            self.append_if_consistent(data, la, 'AR/RA', global_matrix[0][1])
            # self.append_if_consistent(data, la, 'RA', global_matrix[1][0])
            self.append_if_consistent(data, la, 'RR', global_matrix[0][1])

        data = pd.DataFrame(data)
        ax = sns.lineplot(x='Lambda', y='Proportion of cured patients', hue='Strategy', data=data, ax=ax)
        [ax.lines[i].set_linestyle("--") for i in [0, 2]]

        if ax is not None:
            ax.set_title('N = ' + str(n))


if __name__ == '__main__':
    # D2BGlobalPlot().show('../../../images/regulation/Hospital with D2B regulation Global Equ')
    D2BGlobalPlot().lin_plot([1, 1])
    plt.show()
