from enum import Enum
from common import *
from simulation.transportation.dist_per_km import dist_per_km
from scipy.spatial import KDTree


class DayType(Enum):
    workday = 1
    weekend = 2


class TimeInterval(Enum):
    night = 1
    morning = 2
    day = 3
    evening = 4


class CityGraph:
    def __init__(self):
        self.graph = {}
        for day in DayType:
            self.graph[day.value] = {}
            for time in TimeInterval:
                self.graph[day.value][time.value] = self.load_graph(day, time)

    def load_graph(self, day: DayType, time: TimeInterval):
        df = pd.read_csv('../../data/transportation/aggr/spb-%s-%s.csv' % (day.value, time.value), encoding='UTF-8')
        duration_graph = {}
        for row in df.iterrows():
            duration_graph[row['Широта (от)']]


class Graph:
    def __init__(self, day, time):
        df = pd.read_csv('../../data/transportation/aggr/spb-%s-%s.csv' % (day, time), encoding='UTF-8')
        self.velocity = dist_per_km(day, time)
        self.graph = self.build_graph(df)
        self.vertex_tree = self.build_kd_tree()

    def build_graph(self, df):
        g = {}
        for i, row in df:
            x_lat = row['Широта (от)']
            x_lon = row['Долгота (от)']
            y_lat = row['Широта (до)']
            y_lon = row['Долгота (до)']
            duration = row['Длительность (сек)']
            x = (x_lat, x_lon)
            y = (y_lat, y_lon)
            if x not in g:
                g[x] = {}
            g[x][y] = duration / 60
        return g

    def build_kd_tree(self):
        self.vertex = np.asarray(self.graph.keys())
        return KDTree(self.vertex)

    def dist(self, source, destination):
        dist, idx = self.vertex_tree.query([source])
        duration_to_source =
