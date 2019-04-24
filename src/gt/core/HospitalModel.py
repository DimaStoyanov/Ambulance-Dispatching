from src.common import *


class HospitalModel:
    def __init__(self, l, mu, n, N_lim, t_c):
        self._lambda = l
        self._mu = mu
        self._n = n
        self._N_lim = N_lim
        self._t_c = t_c

    def __ro(self, l: int, mu: int, n=None):
        return l / mu if n is None else l / mu / n

    def empty_queue(self, l, n):
        p = 1
        ro = self.__ro(l, self._mu)
        for j in range(1, n + 1):
            p += (ro ** j) / factor(j)
        add_ro = 0
        for j in range(n, self._N_lim):
            add_ro += (ro / n) ** j
        p += (ro ** n) / (factor(n) * add_ro - n)
        return p

    def k_in_queue(self, l, k, n):
        p_0 = self.empty_queue(l, n)
        ro = self.__ro(l, self._mu, n)
        return (ro ** k) * p_0

    def queue_length(self, l, n):
        p_0 = self.empty_queue(l, n)
        ro = self.__ro(l, self._mu, n)
        return (ro ** (n + 1)) / factor(n) * n / ((n - ro) ** 2) * p_0

    def queue_processing_time(self, l, n):
        L = self.queue_length(l, n)
        return L / l + 1 / self._mu

    def p_rej(self, l, n):
        p_0 = self.empty_queue(l, n)
        return self.__ro(l, self._mu) ** self._N_lim / factor(n) / n ** (self._N_lim - n) * p_0

    def __lambda_rr_sup(self, l):
        l_r1 = [l[0] * self.p_rej(l[0], self._n[0]), l[1] * self.p_rej(l[1], self._n[1])]
        l_r2 = [l_r1[1] * self.p_rej(l[0] + l_r1[1], self._n[0]), l_r1[0] * self.p_rej(l[1] + l_r1[0], self._n[1])]
        l_i_1 = np.array([l[0] - l_r1[0], l[1] - l_r1[1]])
        l_i_2 = np.array([l_r1[1] - l_r2[0], l_r1[0] - l_r2[1]])
        l_i_3 = 0.5 * np.array([l_r2[0] + l_r2[1], l_r2[1] + l_r2[0]])
        return l_i_1, l_i_2, l_i_3

    def lambdas(self, type):
        l = np.array([self._lambda / 2, self._lambda / 2])

        if type == 'AA':
            return l
        elif type == 'RA':
            return np.array([l[0] * (1 - self.p_rej(l[0], self._n[0])), l[1] + l[0] * self.p_rej(l[0], self._n[0])])
        elif type == 'AR':
            return np.array([l[0] + l[1] * self.p_rej(l[1], self._n[1]), l[1] * (1 - self.p_rej(l[1], self._n[1]))])
        elif type == 'RR':
            return sum(self.__lambda_rr_sup(l))

    def t_transp(self, lambdas, type, i=None):
        if type == 'AA' or (type == 'RA' and i == 0) or (type == 'AR' and i == 1):
            return 0.25 * self._t_c
        elif (type == 'AR' and i == 0) or (type == 'RA' and i == 1):
            return self._t_c * (1 - 1 / 2 / (1 + self.p_rej(lambdas[1 - i], self._n[i])))
        elif type == 'RR':
            l_sup = [self._lambda / 2, self._lambda / 2]
            l_i_1, l_i_2, l_i_3 = self.__lambda_rr_sup(l_sup)
            return self._t_c * (0.25 * l_i_1[i] + 0.75 * l_i_2[i] + 0.5 * l_i_3[i]) / lambdas[i]

    def total_time(self, lambdas, type):
        t_1 = self.queue_processing_time(lambdas[0], self._n[0])
        t_2 = self.queue_processing_time(lambdas[1], self._n[1])
        t_transp_1 = self.t_transp(lambdas, type, 0)
        t_transp_2 = self.t_transp(lambdas, type, 1)
        return np.array([t_1 + t_transp_1, t_2 + t_transp_2])

    def utility_function(self, l, t):
        return l / t

    def global_average_time_function(self, l, t):
        return np.sum(l * t, 2) / np.sum(l, 2)

    def __lambdas_and_times(self):
        lambdas = np.array([[self.lambdas('AA'), self.lambdas('AR')], [self.lambdas('RA'), self.lambdas('RR')]])
        times = np.array([
            [self.total_time(lambdas[0][0], 'AA'), self.total_time(lambdas[0][1], 'AR')],
            [self.total_time(lambdas[1][0], 'RA'), self.total_time(lambdas[1][1], 'RR')]
        ])
        return lambdas, times

    def game_matrix(self):
        lambdas, times = self.__lambdas_and_times()
        return self.utility_function(lambdas, times)

    def global_average_time_matrix(self):
        lambdas, times = self.__lambdas_and_times()
        return self.global_average_time_function(lambdas, times)
