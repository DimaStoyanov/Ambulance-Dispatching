from simulation.stats.SimulationStats import SimulationStats
from src.common import *


def record_for_each_patient_global(ax, strategy, mu, l=25, ylim=None, queue_buffer=5):
    data = {
        'Transporation time': [],
        'Serving time': [],
        'Queuing time': [],
        'Patient id': []

    }
    stats = SimulationStats(l, [2, 3, 4], strategy, mu=mu)
    for patient, id in zip(stats.patients, range(len(stats.patients))):
        data['Transporation time'].append(patient.transp_time)
        data['Serving time'].append(patient.serve_time)
        data['Queuing time'].append(patient.queue_time)
        data['Patient id'].append(id)
    data = pd.DataFrame(data)
    sns.set(style="whitegrid")
    sns.set_color_codes("pastel")
    ax.set_title('Time record for each patient in system with strategy ' + strategy)
    print(data.tail(10))
    sns.barplot(x="Patient id", y='Transporation time',
                label="Transporation time", data=data, ax=ax, color='b')
    sns.barplot(x="Patient id", y='Serving time', color='g', label='Serving time', data=data, ax=ax)
    sns.set_color_codes('muted')
    sns.barplot(x="Patient id", y='Queuing time', color='r', label='Queuing time', data=data, ax=ax)

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="upper right", frameon=True)
    ax.set(xlim=(0, 50), ylabel="", ylim=ylim, xlabel="Patient id")
    sns.despine(left=True, bottom=True)


if __name__ == '__main__':
    l = 10
    mu = 80
    queue_buffer = 3
    ylim = (0, 500)
    _, axs = plt.subplots(ncols=2, figsize=(25, 5))
    record_for_each_patient_global(axs[0], 'AAA', mu, ylim=ylim, queue_buffer=queue_buffer, l=l)
    record_for_each_patient_global(axs[1], 'RRR', mu, ylim=ylim, queue_buffer=queue_buffer, l=l)
    plt.show()
