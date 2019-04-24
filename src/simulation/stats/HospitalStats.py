class HospitalStats:
    def __init__(self, appeared, served, patients):
        self.appeared = appeared
        self.served = served
        self.patients = patients

    def __repr__(self):
        return 'HospitalStats: {\n' + \
               '    appeared=' + str(self.appeared) + '\n' + \
               '    served=' + str(self.served) + '\n' \
               + '}'
