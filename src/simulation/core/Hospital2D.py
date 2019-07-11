from simulation.core.PatientQueue import *


class Hospital2D:
    def __init__(self, strategy, location, servers_number, hosp_num, queue_buffer=5, velocity=20):
        self.strategy = strategy
        self.location = location
        self.servers_number = servers_number
        self.velocity = velocity
        self.hosp_num = hosp_num
        self.queue_buffer = queue_buffer
        self.served = 0
        self.appeared = 0
        self.queue = Queue(servers_number)
        self.patients = []

    def can_accept_patient(self):
        if self.strategy == 'A':
            return True
        return self.queue.length() < self.queue_buffer

    def get_served_patients(self):
        return [patient for patient in self.patients if patient.queue_time is not None]

    def expected_travel_and_queue_time(self, patient):
        patient.set_transp_time(self.calc_transp_time(patient))
        queue_time = self.queue.calc_expected_queue_time(patient.arrival_time)
        return patient.transp_time + queue_time

    def calc_transp_time(self, patient):
        return self.location.dist(patient.request_location) / self.velocity

    def add_patient(self, patient):
        self.patients.append(patient)
        self.queue.add_patient(patient)
        self.appeared += 1
        return self.queue
