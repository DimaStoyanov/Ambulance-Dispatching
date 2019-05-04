from simulation.stats.SimulationStats import SimulationStats
from src.common import *


def record_for_each_patient(hosp_num, stats, ax, servers, strategy, ylim=None, xlim=None):
    data = {
        'Transporation time': [],
        'Serving time': [],
        'Queuing time': [],
        'Patient id': []

    }
    for patient, id in zip(stats.hospitals[hosp_num].patients, range(len(stats.hospitals[hosp_num].patients))):
        data['Transporation time'].append(patient.transp_time)
        data['Serving time'].append(patient.serve_time)
        data['Queuing time'].append(patient.queue_time)
        data['Patient id'].append(id)
    data = pd.DataFrame(data)
    sns.set(style="whitegrid")
    sns.set_color_codes("pastel")
    ax.set_title('Time record in H%d[server=%d] with strategy %s' % (hosp_num, servers[hosp_num], strategy))
    sns.barplot(x="Patient id", y='Transporation time',
                label="Transporation time", data=data, ax=ax, color='b')
    sns.barplot(x="Patient id", y='Serving time', color='g', label='Serving time', data=data, ax=ax)
    sns.set_color_codes('muted')
    sns.barplot(x="Patient id", y='Queuing time', color='r', label='Queuing time', data=data, ax=ax)

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="upper right", frameon=True)
    ax.set(xlim=xlim, ylabel="", ylim=ylim, xlabel="Patient id")
    sns.despine(left=True, bottom=True)


if __name__ == '__main__':
    mu = 80
    queue_buffer = 5
    ylim = (0, 800)
    xlim = (0, 30)
    l = 10
    servers = [2, 3, 4]
    aaa_stats = SimulationStats(l, [2, 3, 4], 'AAA', mu=mu, queue_buffer=queue_buffer)
    rrr_stats = SimulationStats(l, [2, 3, 4], 'RRR', mu=mu, queue_buffer=queue_buffer)
    _, axs = plt.subplots(ncols=2, nrows=3, figsize=(25, 25))
    for i in range(3):
        record_for_each_patient(i, aaa_stats, axs[i][0], servers, 'AAA', ylim, xlim)
        record_for_each_patient(i, rrr_stats, axs[i][1], servers, 'RRR', ylim, xlim)
    plt.savefig('../../images/Patient time record in each hospital')
    plt.show()
