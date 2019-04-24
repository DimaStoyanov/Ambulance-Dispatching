from gt.core.HospitalModel import *


def global_plot(n, ax):
    data = {
        'Patients Inflow': [],
        'Global time': [],
        'Strategy': []
    }
    l_space = np.linspace(0.1, 0.8, 100)
    for l in l_space:
        hospital = HospitalModel(l, 1, n, N_lim, t_c)
        G = hospital.global_average_time_matrix()
        data['Patients Inflow'].append(l)
        data['Global time'].append(G[0][0])
        data['Strategy'].append('AA')

        data['Patients Inflow'].append(l)
        data['Global time'].append(G[0][1])
        data['Strategy'].append('AR')

        data['Patients Inflow'].append(l)
        data['Global time'].append(G[1][0])
        data['Strategy'].append('RA')

        data['Patients Inflow'].append(l)
        data['Global time'].append(G[1][1])
        data['Strategy'].append('RR')
    data = pd.DataFrame(data)
    sns.lineplot(x="Patients Inflow", y="Global time", hue="Strategy", data=data, ax=ax)
    ax.set_title('Server N = ' + str(n))


fig, axs = plt.subplots(ncols=3, figsize=(20, 5))
global_plot([2,1], axs[0])
global_plot([2,2], axs[1])
global_plot([2,3], axs[2])
plt.show()
