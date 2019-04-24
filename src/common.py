import nashpy as nash
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

t_c = 10
N_lim = 3

def factor(x):
    ans = 1
    while x > 1:
        ans *= x
        x -= 1
    return ans
