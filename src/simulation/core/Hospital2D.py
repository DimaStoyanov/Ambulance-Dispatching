from simulation.core.PatientQueue import *


class Hospital2D:
    def __init__(self, strategy, location, servers_number, queue_buffer, velocity):
        self.strategy = strategy
        self.location = location
        self.servers_number = servers_number
        self.velocity = velocity
        self.queue_buffer = queue_buffer
        self.served = 0
        self.appeared = 0
        self.servers_queue = [Queue() for _ in range(servers_number)]
        self.patients = []

    def can_accept_patient(self, time):
        if self.strategy == 'A':
            return True
        return self.find_shortest_queue(time).length(time) < self.queue_buffer

    def find_shortest_queue(self, time):
        return min(self.servers_queue, key=lambda queue: queue.length(time))

    def calc_queue_time(self, patient):
        return self.find_shortest_queue(patient.arrival_time).calc_expected_queue_time(patient.arrival_time)

    def expected_travel_and_queue_time(self, patient):
        patient.set_transp_time(self.calc_transp_time(patient))
        queue_time = self.find_shortest_queue(patient.arrival_time).calc_expected_queue_time(patient.arrival_time)
        return patient.transp_time + queue_time

    def calc_transp_time(self, patient):
        return self.location.dist(patient.request_location) / self.velocity

    def add_patient(self, patient):
        patient.set_queue_time(self.calc_queue_time(patient))
        self.patients.append(patient)
        queue = self.find_shortest_queue(patient.arrival_time)
        queue.add_patient(patient)
        self.appeared += 1
        return queue
