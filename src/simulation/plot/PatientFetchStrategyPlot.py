from simulation.core.Hospitals2DModel import *
from src.common import *


def fetch_strategy_stats(strategy='RRR', mu=150, ax=None, hosp_num=None):
    model = Hospitals2DModel(4, [2,3,4], strategy, mu=mu)
    freq = {}
    patients = model.patients if hosp_num == None else model.hospitals[hosp_num].patients
    for patient in patients:
        if patient.fetch_strategy not in freq:
            freq[patient.fetch_strategy] = 0
        freq[patient.fetch_strategy] += 1
    data = {
        'Strategy': [],
        'Frequency':[]
    }
    for strategy, count in freq.items():
        data['Strategy'].append(strategy)
        data['Frequency'].append(count)
    data = pd.DataFrame(data)
    sns.barplot(x="Strategy", y='Frequency', label='Strategy frequency', data=data, ax=ax)
    if ax is not None:
        ax.set_title('Global' if hosp_num == None else ('Hospital ' + str(hosp_num + 1)))


if __name__ == '__main__':
    plt.figure()
    _, ax = plt.subplots(figsize=(25, 5))
    fetch_strategy_stats('RRR', ax=ax)
    _, axs = plt.subplots(ncols=3, figsize=(20, 5))
    fetch_strategy_stats('RRR', ax=axs[0], hosp_num=0)
    fetch_strategy_stats('RRR', ax=axs[1], hosp_num=1)
    fetch_strategy_stats('RRR', ax=axs[2], hosp_num=2)
    plt.savefig('../../images/Select Hospital Algorithm')
    plt.show()
