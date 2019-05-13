from common import *


def fix_cities(line):
    line = line.replace('Сестрорецк,', 'Сестрорецк.')
    line = line.replace('Металлострой,', 'Металлострой.')
    line = line.replace('Парголово,', 'Парголово.')
    line = line.replace('Пушкин,', 'Пушкин.')
    line = line.replace('Шушары,', 'Шушары.')
    return line


if __name__ == '__main__':
    data = pd.read_csv('../../data/spb-hourly-fixed.csv', sep='[,;]|--', encoding='UTF-8')
    print(data.head())

    # with open('../../data/spb-hourly.csv', 'r', encoding='UTF-8') as rf:
    #     with open('../../data/spb-hourly-fixed.csv', 'w', encoding='UTF-8') as wf:
    #         for line in rf:
    #             wf.write(fix_cities(line))

