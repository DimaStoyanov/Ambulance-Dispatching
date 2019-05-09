from sortedcontainers import SortedList


class Queue:
    def __init__(self, servers):
        self.servers = servers
        self.queue = SortedList([], key=lambda patient: patient.arrival_time)
        self.served = 0
        self.load = [0]
        self.arrival_times = [0]

    def length(self, request_time):
        return sum([1 for patient in self.queue if patient.arrival_time <= request_time < patient.serve_start_time])

    def add_patient(self, patient):
        self.queue.add(patient)
        self.load.append(self.load[-1] + 1)
        patient.set_queue_state(self.load[-1])
        self.arrival_times.append(patient.arrival_time)

    def pop(self, patient):
        self.served += 1
        self.queue.pop(0)
        self.load.append(self.load[-1] - 1)
        self.arrival_times.append(patient.serve_finish_time)

    def calc_expected_queue_time(self, requested_time):
        patients_in_period = [patient for patient in self.queue
                              if patient.arrival_time <= requested_time < patient.serve_finish_time]
        queue = [patient for patient in patients_in_period if patient.serve_start_time > requested_time]
        serving = [patient for patient in patients_in_period if patient.serve_start_time <= requested_time]
        cur_serve_finish_time = requested_time if not serving else \
            min(serving, key=lambda patient: patient.serve_finish_time).serve_finish_time
        if len(serving) < self.servers:
            return 0
        return cur_serve_finish_time - requested_time + sum(map(lambda p: p.serve_time, queue))
