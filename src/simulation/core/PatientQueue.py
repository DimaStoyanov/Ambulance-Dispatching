from sortedcontainers import SortedList
from common import *
import math


class Queue:
    def __init__(self, servers):
        self.servers = servers
        self.queue = SortedList([], key=lambda patient: patient.arrival_time)
        self.serving = SortedList([], key=lambda patient: patient.serve_finish_time)
        self.served = 0
        self.load = [0]
        self.event_times = [0]

    def length(self):
        return len(self.queue)

    def add_patient(self, patient):
        self.queue.add(patient)
        self.load.append(self.load[-1] + 1)
        patient.set_queue_state(self.load[-1])
        self.event_times.append(patient.arrival_time)

    def start_serving(self):
        if self.queue:
            if len(self.serving) > self.servers:
                raise Exception('All surgeons are busy')
            patient = self.queue.pop(0)
            self.serving.add(patient)

    def finish_serving(self):
        self.served += 1
        patient = self.serving.pop(0)
        self.event_times.append(patient.serve_finish_time)
        self.load.append(self.load[-1] - 1)
        if self.queue:
            return self.queue[0]

    def calc_expected_queue_time(self, requested_time):
        surgeon_times = 0 if not self.serving else np.mean([p.serve_finish_time - requested_time for p in self.serving])
        serve_times_in_queue = []
        for i in range(math.ceil(len(self.queue) / 3)):
            serve_times_in_queue.append(np.mean([p.serve_time for p in self.queue[3 * i:3 * (i + 1)]]))
        return surgeon_times + sum(serve_times_in_queue)
