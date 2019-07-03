from sortedcontainers import SortedList


class Queue:
    def __init__(self, servers):
        self.servers = servers
        self.queue = SortedList([], key=lambda patient: patient.arrival_time)
        self.served = 0
        self.load = [0]
        self.event_times = [0]

    def length(self, request_time):
        return sum([1 for patient in self.queue if patient.arrival_time <= request_time
                    and not patient.serve_finish_time])

    def add_patient(self, patient):
        self.queue.add(patient)
        self.load.append(self.load[-1] + 1)
        patient.set_queue_state(self.load[-1])
        self.event_times.append(patient.arrival_time)

    def pop(self):
        if self.queue:
            self.served += 1
            patient = self.queue.pop(0)
            self.event_times.append(patient.serve_finish_time)
            self.load.append(self.load[-1] - 1)
        for patient in self.queue:
            if not patient.serve_finish_time:
                return patient

    def calc_expected_queue_time(self, requested_time):
        patients_in_period = [patient for patient in self.queue
                              if patient.arrival_time <= requested_time]
        surgeon_finish_time = [0 for _ in range(self.servers)]
        for patient, i in zip(patients_in_period, range(len(patients_in_period))):
            if i < self.servers:
                if patient.serve_finish_time:
                    surgeon_finish_time[i] = patient.serve_finish_time
                else:
                    surgeon_finish_time[i] = patient.arrival_time + patient.serve_time
            else:
                idx = surgeon_finish_time.index(min(surgeon_finish_time))
                surgeon_finish_time[idx] += patient.serve_time
        return min(surgeon_finish_time) - requested_time
