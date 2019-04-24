class Event:
    def __init__(self, event_type, patient, time, queue=None, hospital=None):
        self.type = event_type
        self.patient = patient
        self.time = time
        self.queue = queue
        self.hospital = hospital

