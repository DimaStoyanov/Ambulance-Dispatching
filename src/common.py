import nashpy as nash
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

t_c = 20
N_lim = 3

mu_min = 1 / 40
mu_max = 1 / 5

la_min = 1 / 40
la_max = 1 / 5

points = 20

cost_transp = 3
cost_op = 10
palette = {
    'Inconsistent': 'C9',
    'AA, RR': 'C1',
    'RR, AA': 'C1',
    'AA': 'C5',
    'AR': 'C2',
    'RA': 'C3',
    'RR': 'C4',
    'AR, RA': 'C6',
    'AR, RR': 'C7',
    'RA, RR': 'C8',
    'AA, RA': 'tab:pink',
    'AA, AR': 'tab:olive',
    'RA, AR': 'g'
}

disp_palette = {
    'Inconsistent': 'C9',
    'BE': 'C1',
    'N1-RR,BE': 'C2',
    'N2-RR,BE': 'C3',
    'BE,N1-RR': 'C4',
    'BE,N2-RR': 'C5',
    'BE,N1-RR,N2-RA': 'C6',
    'BE,N1-RA,N2-RA': 'C7',
    'BE,N2-RA,N1-RA': 'C8',
    'N2-RA,BE,N1-RA': 'C7',
    'N2-RA,BE,N1-RR': 'C6',
    'N1-RA,N2-RA,BE': 'C7',
    'N1-RR,N2-RA,BE': 'C6',
    'N1-RR,BE,N2-RA': 'C6',
    'N1-RA,BE,N2-RA': 'C7',
    'BE,N1-RR,N2-AR': 'C0',
    'BE,N1-AR,N2-AR': 'k',
    'BE,N1-RA,N2-RR': 'r',
    'BE,N1-AR,N2-RR': 'C7'
}

disp2str_palette = {
    'Inconsistent': 'tab:grey',
    'N1-RR': 'C0',
    'N1-AA,N1-RR,N2-AA': 'C1',
    'N1-AA,N2-AA': 'C2',
    'N1-RR,N2-RA': 'C3',
    'N1-RA,N2-RA': 'C4',
    'N1-AR,N2-AR': 'C5',
    'N1-RR,N2-AR': 'C6',
    'N2-RR': 'C7',
    'N1-RA,N2-RR': 'C8',
    'N1-AR,N2-RR': 'g',
    'N2-RA': 'b',
    'N1-RA': 'tab:pink',
    'N2-AR': 'tab:cyan',
    'N2-AA': 'tab:olive'
}

revenue = 20

heat_map_palette = []


def build_heat_map_palette():
    for r in np.linspace(0, 1, 100):
        for g in np.linspace(0, 1, 100):
                heat_map_palette.append((r, g, 0))


build_heat_map_palette()


def factor(x):
    ans = 1
    while x > 1:
        ans *= x
        x -= 1
    return ans
