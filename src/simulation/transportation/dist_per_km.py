import mpu
import numpy as np
import pandas as pd


def dist(x_lat, x_lon, y_lat, y_lon):
    return mpu.haversine_distance((x_lat, x_lon), (y_lat, y_lon))


def dist_per_km(day, time):
    df = pd.read_csv('../../data/transportation/aggr/spb-%s-%s.csv' % (day, time), encoding='utf-8', index_col=0)
    dur_per_km = []
    for i, row in df.iterrows():
        x_lat = row['Широта (от)']
        x_lon = row['Долгота (от)']
        y_lat = row['Широта (до)']
        y_lon = row['Долгота (до)']
        duration = row['Длительность (сек)']
        dur_per_km.append(duration / dist(x_lat, x_lon, y_lat, y_lon))
        return np.mean(dur_per_km)


if __name__ == '__main__':
    print('weekend day', dist_per_km('weekend', 'day'))
    print('workday day', dist_per_km('workday', 'day'))
    print('workday night', dist_per_km('workday', 'night'))
    print('weekend morning', dist_per_km('weekend', 'morning'))
    print('workday morning', dist_per_km('workday', 'morning'))
    print('workday evening', dist_per_km('workday', 'evening'))
