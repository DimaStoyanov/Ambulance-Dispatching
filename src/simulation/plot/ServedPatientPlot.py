from simulation.stats.SimulationStats import SimulationStats
from src.common import *


def served_and_appeared_patients_plot(n, ax, mu=50, queue_buffer=5):
    data = {
        'The number of patients appeared': [],
        'The number of patients served in system': [],
        'Strategy': []
    }
    l_space = np.linspace(6, 40, 30)
    strategies = ['AAA', 'ARA', 'AAR', 'ARR', 'RAA', 'RRA', 'RAR', 'RRR']
    # strategies = ['AAA', 'RRR']
    for strategy in strategies:
        for lambda_inflow in l_space:
            stats = SimulationStats(lambda_inflow, n, strategy, mu=mu, queue_buffer=queue_buffer)
            appeared, served = stats.appeared, stats.served
            data['The number of patients appeared'].append(appeared)
            data['The number of patients served in system'].append(served)
            data['Strategy'].append(strategy)

    data = pd.DataFrame(data)
    sns.lineplot(x="The number of patients appeared", y='The number of patients served in system',
                 hue="Strategy", data=data, ax=ax, palette='bright')
    ax.set_title('Server N = ' + str(n))
    [ax.lines[i].set_linestyle("--") for i in range(len(strategies))]


if __name__ == '__main__':
    _, ax = plt.subplots()
    salary = 100_000
    served_and_appeared_patients_plot([2, 3, 4], ax, mu=100)
    plt.show()
    # model = Hospitals2DModel(10, [2, 3, 4], 'RRR', mu=100)
    # patient = model.hospitals[0].all_patients[5]
    # print(patient.transp_time, patient.queue_time, patient.serve_time)
