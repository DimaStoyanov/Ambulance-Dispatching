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

    def __repr__(self):
        return 'Patient reqT=%d arrT=%d ssT=%d sfT=%d' % (self.request_time, self.arrival_time,
                                                          self.serve_start_time, self.serve_finish_time)

    def set_transp_time(self, transp_time):
        self.transp_time = transp_time
        self.arrival_time = self.request_time + transp_time

    def set_queue_time(self, queue_time):
        self.queue_time = queue_time
        self.serve_start_time = self.arrival_time + queue_time
        self.serve_finish_time = self.serve_start_time + self.serve_time
