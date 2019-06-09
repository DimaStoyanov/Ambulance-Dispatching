from src.common import *


class HospitalsModel:
    def __init__(self, la, mu, n, N_lim, t_c, inconsistent_system_threshold=30):
        self.la = la
        self.mu = mu
        self.n = n
        self.N_lim = N_lim
        self.t_c = t_c
        self.inconsistent_system_threshold = inconsistent_system_threshold

    @staticmethod
    def load_param(la, mu):
        return la / mu

    def empty_queue(self, l, n):
        p = 1
        ro = self.load_param(l, self.mu)
        for j in range(1, n):
            p += (ro ** j) / factor(j)
        p += (ro ** n) / factor(n - 1) / (n - ro)
        p **= -1
        if p < 0 or p > 1:
            raise InconsistentSystemException('Probability should be in range from 0 to 1, but actual {}'.format(p))
        return p

    def k_in_queue(self, l, k, n):
        p_0 = self.empty_queue(l, n)
        ro = self.load_param(l, self.mu)
        p = (ro ** k) / factor(k) * p_0

        if p < 0 or p > 1:
            raise InconsistentSystemException('Probability should be in range from 0 to 1, but actual {}'.format(p))
        return p

    def queue_length(self, l, n):
        p_0 = self.empty_queue(l, n)
        ro = self.load_param(l, self.mu)
        return (ro ** (n + 1) * n) / factor(n) / ((n - ro) ** 2) * p_0

    def queue_time(self, la, n):
        return 0 if la == 0 else self.queue_length(la, n) / la

    def queue_processing_time(self, l, n):
        W_q = self.queue_length(l, n)
        if W_q >= self.inconsistent_system_threshold:
            raise InconsistentSystemException('Queue unlimited increases')
        return W_q / l + 1 / self.mu

    def p_rej(self, l, n):
        p_0 = self.empty_queue(l, n)
        p_k = []
        for k in range(1, n + self.N_lim + 1):
            p_k.append(self.k_in_queue(l, k, n))
        return 1 - p_0 - sum(p_k)

    def lambda_rr_sup(self, la):
        l_r1 = [la[0] * self.p_rej(la[0], self.n[0]), la[1] * self.p_rej(la[1], self.n[1])]
        l_r2 = [l_r1[1] * self.p_rej(la[0] + l_r1[1], self.n[0]), l_r1[0] * self.p_rej(la[1] + l_r1[0], self.n[1])]
        l_i_1 = np.array([la[0] - l_r1[0], la[1] - l_r1[1]])
        l_i_2 = np.array([l_r1[1] - l_r2[0], l_r1[0] - l_r2[1]])
        l_i_3 = 0.5 * np.array([l_r2[0] + l_r2[1], l_r2[1] + l_r2[0]])
        return l_i_1, l_i_2, l_i_3

    def lambdas(self, type):
        la = np.array([self.la / 2, self.la / 2])

        try:
            if type == 'AA':
                return la
            elif type == 'RA':
                return np.array(
                    [la[0] * (1 - self.p_rej(la[0], self.n[0])), la[1] + la[0] * self.p_rej(la[0], self.n[0])])
            elif type == 'AR':
                return np.array(
                    [la[0] + la[1] * self.p_rej(la[1], self.n[1]), la[1] * (1 - self.p_rej(la[1], self.n[1]))])
            elif type == 'RR':
                return sum(self.lambda_rr_sup(la))
        except InconsistentSystemException:
            return np.array([np.nan, np.nan])

    def t_transp(self, lambdas, type, i=None):
        if type == 'AA' or (type == 'RA' and i == 0) or (type == 'AR' and i == 1):
            return 0.25 * self.t_c
        elif (type == 'AR' and i == 0) or (type == 'RA' and i == 1):
            return self.t_c * (1 - 1 / 2 / (1 + self.p_rej(lambdas[1 - i], self.n[i])))
        elif type == 'RR':
            l_sup = [self.la / 2, self.la / 2]
            l_i_1, l_i_2, l_i_3 = self.lambda_rr_sup(l_sup)
            return self.t_c * (0.25 * l_i_1[i] + 0.75 * l_i_2[i] + 0.5 * l_i_3[i]) / lambdas[i]

    def total_time(self, lambdas, type):
        try:
            t_1 = self.queue_processing_time(lambdas[0], self.n[0])
            t_2 = self.queue_processing_time(lambdas[1], self.n[1])
            t_transp_1 = self.t_transp(lambdas, type, 0)
            t_transp_2 = self.t_transp(lambdas, type, 1)
            return np.array([t_1 + t_transp_1, t_2 + t_transp_2])
        except InconsistentSystemException:
            return np.array([np.nan, np.nan])

    def lambdas_and_times(self):
        lambdas = np.array([[self.lambdas('AA'), self.lambdas('AR')], [self.lambdas('RA'), self.lambdas('RR')]])
        times = np.array([
            [self.total_time(lambdas[0][0], 'AA'), self.total_time(lambdas[0][1], 'AR')],
            [self.total_time(lambdas[1][0], 'RA'), self.total_time(lambdas[1][1], 'RR')]
        ])
        return lambdas, times

    @staticmethod
    def utility_function(l, t):
        return l / t

    @staticmethod
    def global_average_time_function(l, t):
        return np.sum(l * t, 2) / np.sum(l, 2)

    def game_matrix(self):
        lambdas, times = self.lambdas_and_times()
        return np.nan_to_num(self.utility_function(lambdas, times))

    def global_average_time_matrix(self, nan_to_num=True):
        lambdas, times = self.lambdas_and_times()
        res = self.global_average_time_function(lambdas, times)
        return np.nan_to_num(res) if nan_to_num else res

    def is_system_consistent(self, strategy):
        la = self.lambdas(strategy)
        queue_len = [self.queue_length(la[i], self.n[i]) for i in range(2)]
        return all(la_i > 0 for la_i in la) and all(l < self.inconsistent_system_threshold for l in queue_len)


class InconsistentSystemException(Exception):
    pass


if __name__ == '__main__':
    model = HospitalsModel(1/30, 1/30, [1, 1], 2, 20)
    print(model.lambdas('RR'))
    print(model.game_matrix())
    print(model.global_average_time_matrix())
