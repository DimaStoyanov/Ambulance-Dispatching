from numpy.random import rand
from numpy.random import uniform
import random
import math
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
        alpha = 2 * math.pi * random.random()
        rand_r = r * math.sqrt(random.random())
        x = rand_r * math.cos(alpha)
        y = rand_r * math.sin(alpha)
        return Point2D(x, y)


if __name__ == '__main__':
    print(Point2D.random_point_in_circle(50))
