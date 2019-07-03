from simulation.stats.HospitalStats import *
from simulation.core.Hospitals2DModel import *


class SimulationStats:
    def __init__(self, l, servers, strategies, mu=100, queue_buffer=5, hospitals_count=3, stream=None, iterations=10):
        self.l = l
        self.servers = servers
        self.strategies = strategies
        self.iterations = iterations
        self.mu = mu
        self.stream = stream
        self.queue_buffer = queue_buffer
        self.hospitals_count = hospitals_count
        self.mean_of_simmulations()

    def __repr__(self):
        return 'SimulationStats: {' + \
               '\nappeared=' + str(self.appeared) + \
               '\nserved=' + str(self.served) + \
               '\nhospitals=' + str(self.hospitals) + \
               '\n}'

    def column(self, arr, i):
        return [row[i] for row in arr]

    def aggregate_patient(self, patient_simulations):
        serve_time = np.mean([patient.serve_time for patient in patient_simulations])
        queue_time = np.mean([patient.queue_time for patient in patient_simulations])
        transp_time = np.mean([patient.transp_time for patient in patient_simulations])
        patient = Patient(None, None, serve_time)
        patient.transp_time = transp_time
        patient.queue_time = queue_time
        return patient

    def aggregate_patients(self, patients_simulations):
        # print(len(list(patients_simulations)))
        if not patients_simulations[0]:
            return []
        patients_count = np.min([len(patients_simulation) for patients_simulation in patients_simulations])
        return [self.aggregate_patient(self.column(patients_simulations, i)) for i in range(patients_count)]

    def aggregate_hospital(self, hospital_simulations):
        appeared = np.mean([hospital.appeared for hospital in hospital_simulations])
        served = np.mean([hospital.served for hospital in hospital_simulations])
        patients = self.aggregate_patients([hospital.get_served_patients() for hospital in hospital_simulations])
        return HospitalStats(appeared, served, patients)

    def aggregate_hospitals(self, hospitals_simulations):
        return [self.aggregate_hospital(self.column(hospitals_simulations, i)) for i in range(self.hospitals_count)]

    def mean_of_simmulations(self):
        patients = []
        appeared = []
        served = []
        hospitals = []
        for i in range(self.iterations):
            model = Hospitals2DModel(self.l, self.servers, self.strategies, mu=self.mu, stream=self.stream,
                                     queue_buffer=self.queue_buffer)
            patients.append(model.get_served_patients())
            appeared.append(model.appeared)
            served.append(model.served)
            hospitals.append(model.hospitals)
        self.appeared = np.mean(appeared)
        self.served = np.mean(served)
        self.patients = self.aggregate_patients(patients)
        self.hospitals = self.aggregate_hospitals(hospitals)


if __name__ == '__main__':
    print(SimulationStats(25, [2, 3, 4], 'RRR'))
