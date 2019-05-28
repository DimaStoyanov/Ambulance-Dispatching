from gt.core.HospitalsModel import HospitalsModel
from common import *


class HospitalWith1YM(HospitalsModel):
    def __init__(self, la, mu, n, N_lim, t_c, revenue_cured, med_expences):
        super(HospitalWith1YM, self).__init__(la, mu, n, N_lim, t_c)
        self.revenue_cured = revenue_cured
        self.med_expences = med_expences

    @staticmethod
    def p_mortality(t):
        return (0.00043 * t ** 2 + 0.0045 * t + 2.86) / 100

    def utility_function(self, la, t):
        return la * ((1 - self.p_mortality(t)) * self.revenue_cured - self.med_expences)

    def global_matrix(self):
        lambdas, times = self.lambdas_and_times()
        lambdas_cured = lambdas * (1 - self.p_mortality(times))
        return np.nan_to_num(np.sum(lambdas_cured, axis=2) / np.sum(lambdas, axis=2))


if __name__ == '__main__':
    model = HospitalWith1YM(2, 2, [1, 1], 5, 10, 30, 13)
    print(model.game_matrix())
