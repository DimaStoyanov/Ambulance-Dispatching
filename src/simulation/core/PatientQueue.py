from sortedcontainers import SortedList

class Queue:
    def __init__(self):
        self.queue = SortedList([], key=lambda patient: patient.arrival_time)
        self.served = 0
        self.load = [0]
        self.arrival_times = [0]

    def length(self, request_time):
        return sum([1 for patient in self.queue if patient.arrival_time <= request_time])

    def update_queue(self):
        if self.current_patient is not None and self.current_patient.serve_finish_time <= self.time:
            self.total_patients_served += 1
            self.current_patient = None
        if len(self.queue) > 0 and self.queue[0].serve_start_time <= self.time:
            self.current_patient = self.queue.pop(0)

    def add_patient(self, patient):
        self.queue.add(patient)
        self.load.append(self.load[-1] + 1)
        self.arrival_times.append(patient.arrival_time)

    def pop(self, patient):
        self.served += 1
        self.queue.pop(0)
        self.load.append(self.load[-1] - 1)
        self.arrival_times.append(patient.serve_finish_time)

    def calc_expected_queue_time(self, requested_time):
        queue = [patient for patient in self.queue
                 if patient.arrival_time <= requested_time and patient.serve_finish_time > requested_time]
        if not queue:
            return 0
        else:
            return queue[0].serve_finish_time - requested_time + sum(map(lambda p: p.serve_time, queue))
