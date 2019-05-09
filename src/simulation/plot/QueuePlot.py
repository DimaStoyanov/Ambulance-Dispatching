from src.common import *
from simulation.core.Hospitals2DModel import Hospitals2DModel


def queue_plot(queue, hosp_num, strategy, ax, ylim=None, queue_buffer=5):
    data = {
        'Time': queue.arrival_times + [0, 2000],
        'Load': queue.load + ([queue_buffer] * 2),
        'Type': ['Queue load' for _ in range(len(queue.arrival_times))] + (['Queue buffer'] * 2)
    }
    data = pd.DataFrame(data)
    sns.lineplot(x='Time', y='Load', hue='Type', data=data, ax=ax)
    ax.set_title('Queue load in Hospital {}, Strategy {}'.format(hosp_num + 1, strategy))
    ax.set(ylim=ylim)


if __name__ == '__main__':
    l = 10
    mu = 80
    queue_buffer = 3
    ylim = (0, 15)
    aaa_model = Hospitals2DModel(l, [2, 3, 4], 'AAA', mu=mu, queue_buffer=queue_buffer)
    rrr_model = Hospitals2DModel(l, [2, 3, 4], 'RRR', mu=mu, queue_buffer=queue_buffer)
    ax_index = 0
    for i in range(len(aaa_model.hospitals)):
        plt.figure()
        _, axs = plt.subplots(ncols=2, figsize=(10, 5))
        aaa_queue = aaa_model.hospitals[i].queue
        queue_plot(aaa_queue, i, 'AAA', axs[0], ylim, queue_buffer=queue_buffer)
        rrr_queue = rrr_model.hospitals[i].queue
        queue_plot(rrr_queue, i, 'RRR', axs[1], ylim, queue_buffer=queue_buffer)
        ax_index += 1
        plt.savefig('../../images/Queue load for Hospital {}'.format(i + 1))
        plt.show()
