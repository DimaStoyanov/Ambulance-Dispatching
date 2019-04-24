from numpy.random import rand
from numpy.random import uniform
import numpy as np


class Point2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __repr__(self):
        return '(' + str(self.x) + ';' + str(self.y) + ')'

    @staticmethod
    def random_point_in_circle(r):
        x = uniform(-r, r)
        y2 = (r ** 2) - (x ** 2)
        y = np.sqrt(y2)
        if rand() > 0.5:
            y = -y
        return Point2D(x, y)


if __name__ == '__main__':
    print(Point2D.random_point_in_circle(50))
