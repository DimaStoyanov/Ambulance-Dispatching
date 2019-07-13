from datetime import datetime
from common import *


def fix_cities(line):
    line = line.replace('Сестрорецк,', 'Сестрорецк.')
    line = line.replace('Металлострой,', 'Металлострой.')
    line = line.replace('Парголово,', 'Парголово.')
    line = line.replace('Пушкин,', 'Пушкин.')
    line = line.replace('Шушары,', 'Шушары.')
    line = line.replace(', ', ' ')
    return line


def address_to_coord_from():
    df = pd.read_csv('../../data/transportation/unique_addresses_from.csv', encoding='utf-8')
    coord_by_address = {}

    for idx, line in df.iterrows():
        address = fix_cities(fix_cities(line['Address']))
        coord_by_address[address] = [line['Lon'], line['Lat']]
    return coord_by_address


def address_to_coord_to():
    df = pd.read_csv('../../data/transportation/unique_addresses_to.csv', encoding='utf-8')
    coord_by_address = {}

    for idx, line in df.iterrows():
        address = fix_cities(fix_cities(line['Address']))
        coord_by_address[address] = [line['Lon'], line['Lat']]
    return coord_by_address


coords_from = address_to_coord_from()
coords_to = address_to_coord_to()


def get_data(hour, days):
    with open('../../data/transportation/spb-%02d.csv' % (hour), encoding='utf-8') as f:
        data = f.readlines()
        line_by_addresses = {}
        for row in data[1:]:
            cols = row.split(',')
            date = datetime.strptime(cols[4], '%d.%m.%Y')
            if days.count(date.isoweekday()) > 0:
                key = ','.join(cols[:4])
                if key not in line_by_addresses:
                    line_by_addresses[key] = []
                line_by_addresses[key].append(cols)
        ans = []
        for _, cols_arr in line_by_addresses.items():
            duration = np.mean([int(cols[6]) for cols in cols_arr])
            cols = cols_arr[0]
            from_name = ' '.join(cols[:2])
            if cols[1] == '':
                from_name = from_name[:-1]
            if from_name not in coords_from:
                print(coords_from)
            from_c = coords_from[from_name]
            to_name = ' '.join(cols[2:4])
            to_c = [None] * 2 if to_name not in coords_to else coords_to[to_name]
            ans.append([cols[0], cols[1], str(from_c[0]), str(from_c[1]), cols[2], cols[3], str(to_c[0]), str(to_c[1]), str(duration)])
        return ans


def get_days_num(day_type):
    if day_type == 'workday':
        return [1, 2, 3, 4, 5]
    else:
        return [6, 7]


def get_hours(time_interval):
    if time_interval == 'night':
        return list(range(6))
    elif time_interval == 'morning':
        return list(range(6, 12))
    elif time_interval == 'day':
        return list(range(12, 18))
    else:
        return list(range(18, 24))


def write_data(day_type, time_interval):
    with open('../../data/transportation/spb-%s-%s.csv' % (day_type, time_interval), 'w', encoding='utf-8') as f:
        f.write('Адрес (от),Широта (от),Долгота (от),Адрес (до),Широта (до),Долгота (до),Длительность (сек)\n')
        for hour in get_hours(time_interval):
            for cols in get_data(hour, get_days_num(day_type)):
                f.write(','.join(cols) + '\n')


if __name__ == '__main__':
    write_data('workday', 'night')
    write_data('workday', 'morning')
    write_data('workday', 'day')
    write_data('workday', 'evening')
    write_data('weekend', 'night')
    write_data('weekend', 'morning')
    write_data('weekend', 'day')
    write_data('weekend', 'evening')
