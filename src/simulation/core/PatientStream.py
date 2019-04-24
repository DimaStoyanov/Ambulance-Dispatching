from numpy.random import exponential
from simulation.core.Event import Event
from simulation.core.Patient import Patient
from simulation.core.Point2D import *


class Stream:

    def __init__(self, l, mu, timesteps, r):
        self.l = l
        self.mu = mu
        self.timesteps = timesteps
        self.r = r
        self.events = []
        self.total_patients = 0
        self.generate()

    def create_appear_event(self, time, serve_time):
        loc = Point2D.random_point_in_circle(self.r)
        return Event('appear', Patient(loc, time, serve_time), time)

    def generate(self):
        time = 0
        interval_distr = exponential(self.l, 2000)
        serve_distr = exponential(self.mu, 2001)
        self.interval_mean = np.mean(interval_distr)
        self.events.append(self.create_appear_event(time, serve_distr[0]))
        for interval, serve_time in zip(interval_distr, serve_distr[1:]):
            time += interval
            if time < self.timesteps:
                self.events.append(self.create_appear_event(time, serve_time))
            else:
                break
        self.total_patients = len(self.events)


if __name__ == '__main__':
    a = Stream(25, 50, 2000, 50)
    print('Mean of interval between patient appearing:', a.interval_mean)
    print('Total patients', a.total_patients)
