from common import *
from gt.core.HospitalsModel import HospitalsModel, InconsistentSystemException


class DispatcherAndHospitalsModel(HospitalsModel):

    def __init__(self, la, mu, n, N_lim, t_c, lim_iterations=10):
        super(DispatcherAndHospitalsModel, self).__init__(la, mu, n, N_lim, t_c)
        self.lim_iterations = lim_iterations

    def best_expected_flow(self, la_first, la_second, la_adj_first, la_adj_second):
        la_first_part, la_second_part = la_first / self.lim_iterations, la_second / self.lim_iterations
        la_i_first, la_i_second, la_j_first, la_j_second = 0, 0, 0, 0

        for i in range(self.lim_iterations):
            if (self.queue_time(la_adj_first + la_i_first + la_i_second, self.n[0]) + 0.25 * self.t_c <
                    self.queue_time(la_adj_second + la_j_first + la_j_second, self.n[1]) + 0.75 * self.t_c):
                la_i_first += la_first_part
            else:
                la_j_second += la_first_part
            if (self.queue_time(la_adj_first + la_i_first + la_i_second, self.n[0]) + 0.75 * self.t_c <
                    self.queue_time(la_adj_second + la_j_first + la_j_second, self.n[1]) + 0.25 * self.t_c):
                la_i_second += la_second_part
            else:
                la_j_first += la_second_part

        return np.array([[la_i_first, la_i_second], [la_j_first, la_j_second]])

    def lambda_rr_sup(self, la):
        la_r1 = [la[0] * self.p_rej(la[0], self.n[0]), la[1] * self.p_rej(la[1], self.n[1])]
        la_r2 = [la_r1[1] * self.p_rej(la[0] + la_r1[1], self.n[0]), la_r1[0] * self.p_rej(la[1] + la_r1[0], self.n[1])]
        la_i_1 = np.array([la[0] - la_r1[0], la[1] - la_r1[1]])
        la_i_2 = np.array([la_r1[1] - la_r2[0], la_r1[0] - la_r2[1]])
        return la_r1, la_r2, la_i_1, la_i_2

    def lambdas_and_transp_times_for_RR(self, dispatcher_strategy):
        la_source = [self.la / 2, self.la / 2]
        la_r1, la_r2, la_i1, la_i2 = self.lambda_rr_sup(la_source)
        if dispatcher_strategy == 'N2':
            lambdas_adj = np.array(la_i1) + np.array(la_i2)
            la_be = np.flip(self.best_expected_flow(la_r2[1], la_r2[0], lambdas_adj[1], lambdas_adj[0]), axis=0)
            la = lambdas_adj + np.sum(la_be, axis=1)
            t_transp = np.array([
                (0.25 * (la_i1[0] + la_be[0][1]) + 0.75 * (la_i2[0] + la_be[0][0])) / la[0],
                (0.25 * (la_i1[1] + la_be[1][1]) + 0.75 * (la_i2[1] + la_be[1][0])) / la[1]
            ])
            return la, t_transp

        if dispatcher_strategy == 'N1':
            la_be = self.best_expected_flow(la_r1[0], la_r1[1], la_i1[0], la_i1[1])
            la = la_i1 + np.sum(la_be, axis=1)
            t_transp = np.array([
                (0.25 * (la_i1[0] + la_be[0][0]) + 0.75 * la_be[0][1]) / la[0],
                (0.25 * (la_i1[1] + la_be[1][0]) + 0.75 * la_be[1][1]) / la[1]
            ])
            return la, t_transp

    def lambdas_and_transp_times(self, dispatcher_strategy, hospitals_strategy):
        la_source = [self.la / 2, self.la / 2]

        if dispatcher_strategy == 'BE':
            la_be = self.best_expected_flow(la_source[0], la_source[1], 0, 0)
            la = np.sum(la_be, axis=1)
            t_transp = np.array([
                (0.25 * la_be[0][0] + 0.75 * la_be[0][1]) / la[0],
                (0.25 * la_be[1][0] + 0.75 * la_be[1][1]) / la[1]
            ])
            return la, t_transp

        if hospitals_strategy == 'AA':
            return la_source, np.array([self.t_c / 4, self.t_c / 4])
        if hospitals_strategy == 'RA':
            la = np.array([
                la_source[0] * (1 - self.p_rej(la_source[0], self.n[0])),
                la_source[1] + la_source[0] * self.p_rej(la_source[0], self.n[0])
            ])
            t_transp = np.array([
                self.t_c / 4,
                (0.25 + 0.75 * self.p_rej(self.la / 2, self.n[1])) / (1 + self.p_rej(self.la / 2, self.n[1])),
            ])
            return la, t_transp

        if hospitals_strategy == 'AR':
            la = np.array([
                la_source[0] + la_source[1] * self.p_rej(la_source[1], self.n[1]),
                la_source[1] * (1 - self.p_rej(la_source[1], self.n[1]))
            ])
            t_transp = np.array([
                (0.25 + 0.75 * self.p_rej(self.la / 2, self.n[0])) / (1 + self.p_rej(self.la / 2, self.n[0])),
                self.t_c / 4
            ])
            return la, t_transp

        return self.lambdas_and_transp_times_for_RR(dispatcher_strategy)

    def lambdas_and_times(self):
        lambdas = []
        times = []
        for dispatcher_strategy in ['N2', 'N1', 'BE']:
            lambdas.append([])
            times.append([])
            for hosp_i_strategy in ['A', 'R']:
                lambdas[-1].append([])
                times[-1].append([])
                for hosp_j_strategy in ['A', 'R']:
                    try:
                        la, t_trasnp = self.lambdas_and_transp_times(dispatcher_strategy,
                                                                     hosp_i_strategy + hosp_j_strategy)
                        total_time = np.array([
                            t_trasnp[0] + self.queue_processing_time(la[0], self.n[0]),
                            t_trasnp[1] + self.queue_processing_time(la[1], self.n[1])
                        ])
                        lambdas[-1][-1].append(la)
                        times[-1][-1].append(total_time)
                    except InconsistentSystemException:
                        lambdas[-1][-1].append(np.array([-1e9, -1e9]))
                        times[-1][-1].append(np.array([1e9, 1e9]))

        return np.array(lambdas), np.array(times)

    @staticmethod
    def global_average_time_function_scalar(l, t):
        return np.sum(l) / np.sum(l * t)

    @staticmethod
    def utility_function(l, t):
        return l / t

    def game_matrix(self):
        lambdas, times = self.lambdas_and_times()
        matrix = []
        for i in range(3):
            matrix.append([])
            for j in range(2):
                matrix[i].append([])
                for k in range(2):
                    dispatcher_payoff = self.global_average_time_function_scalar(lambdas[i][j][k], times[i][j][k])
                    hospitals_payoff = self.utility_function(lambdas[i][j][k], times[i][j][k])
                    matrix[i][j].append([dispatcher_payoff, hospitals_payoff[0], hospitals_payoff[1]])
        return np.array(matrix)


if __name__ == '__main__':
    model = DispatcherAndHospitalsModel(2, 2, [2, 1], 3, 10)
    print(model.game_matrix())
