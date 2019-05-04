from simulation.core.PatientStream import Stream
from simulation.stats.StrategiesStats import StrategiesStats
from simulation.stats.SimulationStats import SimulationStats


class ChangeStrategyEquilibriumStats:
    def __init__(self, la, mu, iterations=2, start_strategies='AAA', timesteps=2000, r=50, servers=[2, 3, 4],
                 queue_buffer=5):
        self.la = la
        self.mu = mu
        self.iterations = iterations
        self.timesteps = timesteps
        self.servers = servers
        self.queue_buffer = queue_buffer
        self.start_strategies = start_strategies
        self.r = r
        self.collect_stats()

    def collect_stats(self):
        stream = Stream(self.la, self.mu, self.timesteps, self.r)
        self.strategies_stats = StrategiesStats(self.start_strategies)

        for s1 in ['A', 'R']:
            for s2 in ['A', 'R']:
                for s3 in ['A', 'R']:
                    strategy = s1 + s2 + s3
                    stats = SimulationStats(self.la, self.servers, strategy, self.mu, stream=stream,
                                            queue_buffer=self.queue_buffer, iterations=self.iterations)
                    self.strategies_stats.payoff[strategy] = [round(h.served) for h in stats.hospitals]
        self.nash_equilibrium = self.strategies_stats.get_nash_equilibrium()
