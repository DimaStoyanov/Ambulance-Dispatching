from gt.plot.HospitalGlobalPlot import GlobalEquPlot
from gt.core.HospitalWith1YModel import HospitalWith1YM
from common import *


class M1YGlobalPlot(GlobalEquPlot):
    def global_matrix(self, la, mu, n):
        model = HospitalWith1YM(la, mu, n, N_lim, 1, 13, 13)
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
        mu = 180
        for la in np.linspace(180, 300, 30):
            global_matrix = HospitalWith1YM(la, mu, n, N_lim, 0.005, 13, 13).global_matrix()

            self.append_if_consistent(data, la, 'AA', global_matrix[0][0])
            self.append_if_consistent(data, la, 'AR', global_matrix[0][1])
            self.append_if_consistent(data, la, 'RA', global_matrix[1][0])
            self.append_if_consistent(data, la, 'RR', global_matrix[0][1])

        data = pd.DataFrame(data)
        sns.lineplot(x='Lambda', y='Proportion of cured patients', hue='Strategy', data=data, ax=ax)
        if ax is not None:
            ax.set_title('N = ' + str(n))


if __name__ == '__main__':
    # D2BGlobalPlot().show('../../../images/regulation/Hospital with D2B regulation Global Equ')
    M1YGlobalPlot().lin_plot([1,1])
    plt.show()
