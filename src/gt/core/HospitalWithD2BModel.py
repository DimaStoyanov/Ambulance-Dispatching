from gt.core.HospitalsModel import HospitalsModel
from common import *


class HospitalWithD2BModel(HospitalsModel):
    def __init__(self, la, mu, n, N_lim, t_c, revenue_cured, cost_transp, cost_op):
        super(HospitalWithD2BModel, self).__init__(la, mu, n, N_lim, t_c)
        self.revenue_cured = revenue_cured
        self.cost_transp = cost_transp
        self.cost_op = cost_op

    @staticmethod
    def p_mortality(t):
        return np.minimum(
            (2.83204328e-11 * t ** 5 - 2.11879941e-08 * t ** 4 + 4.61775189e-06 * t ** 3 - 1.91991297e-04 * t ** 2 +
             1.03594973e-02 * t + 2.78396809), [10.3] * len(t)) / 100

    def lambda_cured(self, la, t):
        return la * (1 - self.p_mortality(t))

    def utility_function(self, la, t):
        return self.lambda_cured(la, t) * (self.revenue_cured - self.cost_op) - la * self.cost_transp

    def global_matrix(self):
        lambdas, times = self.lambdas_and_times()
        lambdas_cured = self.lambda_cured(lambdas, times)
        return np.nan_to_num(np.sum(lambdas_cured, axis=2) / np.sum(lambdas, axis=2))

    def actual_total_time(self):
        lambdas, times = self.lambdas_and_times()
        lambdas_cured = self.lambda_cured(lambdas, times)
        times_cured = np.array([
            [self.total_time(lambdas_cured[0][0], 'AA'), self.total_time(lambdas_cured[0][1], 'AR')],
            [self.total_time(lambdas_cured[1][0], 'RA'), self.total_time(lambdas_cured[1][1], 'RR')]
        ])
        return lambdas_cured, times_cured


if __name__ == '__main__':
    model = HospitalWithD2BModel(2, 2, [1, 1], 5, 10, 30, 3, 10)
    print(model.game_matrix())
    print(model.global_matrix())
