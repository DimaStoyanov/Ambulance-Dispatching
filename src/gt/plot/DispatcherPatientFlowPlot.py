from gt.plot.Dispatcher2StrategiesPlot import *

def global_plot(n, ax):
    data = {
        'Patients Inflow': [],
        'Global time': [],
        'Strategy': []
    }
    l_space = np.linspace(0.1, 0.8, 100)
    for l in l_space:
        hospital = DispatcherAndHospitalsModel(l, 1, n, N_lim, t_c)
        G = hospital.global_average_time_matrix()
        for disp_strategy, i in zip(['N2', 'N1'], range(2)):
            for hosp1_strategy, j in zip(['A', 'R'], range(2)):
                for hosp2_strategy, k in zip(['A', 'R'], range(2)):
                    data['Patients Inflow'].append(l)
                    data['Global time'].append(G[i][j][k])
                    data['Strategy'].append(disp_strategy + ';' + hosp1_strategy + hosp2_strategy)

    data = pd.DataFrame(data)
    sns.lineplot(x="Patients Inflow", y="Global time", hue="Strategy", data=data, ax=ax, palette='bright')
    ax.set_title('Server N = ' + str(n))
    [ax.lines[i].set_linestyle("--") for i in range(6)]


if __name__ == '__main__':
    fig, axs = plt.subplots(ncols=3, figsize=(20, 5))
    global_plot([2, 1], axs[0])
    global_plot([2, 2], axs[1])
    global_plot([2, 3], axs[2])
    plt.savefig('../../images/Dispatcher/Patient Inflow')
    plt.show()
