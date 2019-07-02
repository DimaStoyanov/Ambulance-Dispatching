class Patient:
    def __init__(self, request_location, request_time, serve_time):
        self.request_location = request_location
        self.request_time = request_time
        self.serve_time = serve_time
        self.transp_time = None
        self.queue_time = None
        self.arrival_time = None
        self.serve_start_time = None
        self.serve_finish_time = None
        self.fetch_strategy = None
        self.queue_state = None
        self.hospital_num = None

    def __repr__(self):
        return 'Patient reqT=%d arrT=%d ssT=%d sfT=%d hosp=%d fetch=%s' % (self.request_time, self.arrival_time,
                                                          self.serve_start_time, self.serve_finish_time, self.hospital_num, self.fetch_strategy)

    def set_transp_time(self, transp_time):
        self.transp_time = transp_time
        self.arrival_time = self.request_time + transp_time

    def set_queue_time(self, queue_time):
        self.queue_time = queue_time
        self.serve_start_time = self.arrival_time + queue_time
        self.serve_finish_time = self.serve_start_time + self.serve_time

    def set_serve_start_time(self, serve_start_time):
        self.serve_start_time = serve_start_time
        self.queue_time = self.serve_start_time - self.arrival_time
        self.serve_finish_time = self.serve_start_time + self.serve_time

    def set_queue_state(self, state):
        self.queue_state = state

    def set_hosp_num(self, hosp_num):
        self.hospital_num = hosp_num
