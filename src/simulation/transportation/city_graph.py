class CityGraph:
    def __init__(self, ):
        self.hour = hour

    def load_graph(self):
        data = pd.read_csv('../../data/transportation/spb-%02d.csv' % self.hour, encoding='UTF-8')
        print(data.describe())

