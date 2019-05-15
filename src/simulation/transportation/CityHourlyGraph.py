from dijkstar import *
from common import *

class CityHourlyGraph:
    def __init__(self, hour):
        self.hour = hour

    def load_graph(self):
        pd.read_csv('../../data/transportation/spb-%02d.csv' % self.hour, encoding='UTF-8')
        

if __name__ == '__main__':
    graph = Graph()
    graph.add_edge('A', 'B', {'cost': 1})
    graph.add_edge('B', 'C', {'cost': 1})
    print(list(graph.keys()))
    # graph.marshal('kek.txt')
