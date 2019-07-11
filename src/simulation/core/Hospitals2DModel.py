from simulation.core.Hospital2D import *
from simulation.core.PatientStream import *
import pandas as pd


class Hospitals2DModel:
    def __init__(self, lambda_inflow, servers_in_hospital, strategies, mu=1, timesteps=2000,
                 hosp_locations=[Point2D(-25, 25), Point2D(0, -43), Point2D(25, 25)],
                 queue_buffer=10, r=50, velocity=0.5, stream=None):
        self.hospitals = [Hospital2D(strategies[i], hosp_locations[i], servers_in_hospital[i], i,
                                     queue_buffer, velocity) for i in range(len(hosp_locations))]
        self.stream = Stream(lambda_inflow, mu, timesteps, r) if stream is None else stream
        self.appeared = self.stream.total_patients
        self.mu = mu
        self.timesteps = timesteps
        self.queue_buffer = queue_buffer
        self.velocity = velocity
        self.served = 0
        self.patients = []
        self.events = SortedList(self.stream.events, key=lambda event: event.time)
        self.all_events = []
        self.model_queue()

    def __repr__(self):
        return str((self.appeared, self.served))

    def sorted_by_transp_time(self, patient):
        return sorted(self.hospitals, key=lambda hosp: hosp.calc_transp_time(patient))

    def min_by_expected_travel_and_queue_time(self, patient):
        return min(self.hospitals, key=lambda hosp: hosp.expected_travel_and_queue_time(patient))

    def get_served_patients(self):
        return [patient for patient in self.patients if patient.serve_finish_time is not None]

    def distribute_patient(self, patient):
        self.patients.append(patient)
        for hosp, i in zip(self.sorted_by_transp_time(patient), range(len(self.hospitals))):
            patient.set_transp_time(hosp.calc_transp_time(patient))
            if hosp.can_accept_patient():
                patient.set_hosp_num(hosp.hosp_num)
                patient.fetch_strategy = 'Closest Dist ' + str(i + 1)
                self.events.add(Event('arrival', patient, patient.arrival_time, hosp.queue, hosp))
                return
        best_hosp = self.min_by_expected_travel_and_queue_time(patient)
        patient.fetch_strategy = 'Best expected time'
        patient.set_hosp_num(best_hosp.hosp_num)
        self.events.add(Event('arrival', patient, patient.arrival_time, best_hosp.queue, best_hosp))

    def model_queue(self):
        while self.events:
            event = self.events.pop(0)
            self.all_events.append(event)
            if event.time > self.timesteps:
                break
            if event.type == 'appear':
                self.distribute_patient(event.patient)
            elif event.type == 'served':
                new_serving_patient = event.queue.finish_serving()
                self.served += 1
                event.hospital.served += 1
                if new_serving_patient:
                    self.events.add(Event('start_serving', new_serving_patient, event.time,
                                          event.queue, event.hospital))
            elif event.type == 'start_serving':
                event.patient.set_serve_start_time(event.time)
                event.queue.start_serving()
                self.events.add(Event('served', event.patient, event.patient.serve_finish_time,
                                      event.queue, event.hospital))
            elif event.type == 'arrival':
                event.hospital.add_patient(event.patient)
                cur_time = event.time
                if event.queue.load[-1] <= event.queue.servers:
                    self.events.add(Event('start_serving', event.patient, cur_time, event.queue, event.hospital))
        return self.appeared, self.served

    def show_patients(self, from_index=0, until_index=None):
        for event in self.all_events:
            event.patient.events.append(event)
        records = {
            'ID': [],
            'H': [],
            'Queue State': [],
            'RT': [],
            'AT': [],
            'SST': [],
            'SFT': [],
            'FA': [],
            'QT': [],
            'ST': []
        }
        patients = self.patients[from_index:until_index]
        for patient, id in zip(patients, range(len(patients))):
            records['ID'].append(id)
            records['H'].append(patient.hospital_num)
            records['Queue State'].append(patient.queue_state)
            records['RT'].append(patient.request_time)
            records['AT'].append(patient.arrival_time)
            records['SST'].append(patient.serve_start_time)
            records['SFT'].append(patient.serve_finish_time)
            records['QT'].append(patient.queue_time)
            records['ST'].append(patient.serve_time)
            records['FA'].append(patient.fetch_strategy)
        records = pd.DataFrame(records)
        records = records.sort_values('AT')
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.max_rows', 500)

        with open('output.txt', 'w') as f:
            f.write(records.to_string())

        print(f)


if __name__ == '__main__':
    model = Hospitals2DModel(5, [1, 1, 1], 'RRR', mu=100, queue_buffer=2)
    model.show_patients(0, 300)
