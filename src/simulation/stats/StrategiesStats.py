from simulation.stats.SimulationStats import SimulationStats


class StrategiesStats:
    def __init__(self, active_strategies={'AAA'}, la=14, mu=120, servers=[3, 3, 3], iterations=10):
        self.payoff = {}
        self.active_strategies = active_strategies
        self.la = la
        self.mu = mu
        self.servers = servers
        self.iterations = iterations
        self.calc_payoff()

    def calc_payoff(self):
        for s1 in ['A', 'R']:
            for s2 in ['A', 'R']:
                for s3 in ['A', 'R']:
                    strategy = s1 + s2 + s3
                    stats = SimulationStats(self.la, self.servers, strategy, self.mu)
                    self.payoff[strategy] = [round(h.served) for h in stats.hospitals]

    def get_nash_equilibrium(self):
        for i in range(self.iterations):
            for strategy in self.active_strategies:
                alt_strategies = self.get_changed_strategies_for_each_agent(strategy)
                for j in range(len(alt_strategies)):
                    if self.payoff[alt_strategies[j]][j] > self.payoff[strategy][j]:
                        self.active_strategies.remove(strategy)
                        self.active_strategies.add(alt_strategies[j])
        return self.active_strategies

    def get_changed_strategies_for_each_agent(self, strategy):
        return [strategy[:i] + self.changed_strstegy(strategy[i]) + strategy[i + 1:] for i in range(len(strategy))]

    def changed_strstegy(self, strategy):
        return 'R' if strategy == 'A' else 'R'


if __name__ == '__main__':
    model = SimulationStats(12, [3, 3, 3], 'RRR', 120)
    print([round(h.served) for h in model.hospitals])
