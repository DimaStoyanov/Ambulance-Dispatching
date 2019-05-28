from common import *
from datetime import datetime
import re


class SurgeryData:
    def __init__(self):
        self.data = pd.read_csv('../../data/hospitalization.csv', sep=';')
        self.dates = []
        for row in self.data.iterrows():
            date = row[1]['DateTime']
            values = [int(i) for i in re.split('[-T:]+', date)]
            date = datetime(values[0], values[1], values[2], values[3], values[4], values[5])
            self.dates.append(date)

        self.intervals = []
        self.dates = sorted(self.dates)
        for i in range(1, len(self.dates)):
            diff = (self.dates[i] - self.dates[i - 1])
            if diff.days >= 1:
                continue
            self.intervals.append(diff.seconds / 60)
        print(np.mean(self.intervals))
        print(np.std(self.intervals))


if __name__ == '__main__':
    print(SurgeryData().intervals[:5])
