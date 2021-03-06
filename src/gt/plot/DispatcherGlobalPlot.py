from gt.core.HospitalsAndDispatcherModel import *


def global_solution(l, mu, n):
    hospital = DispatcherAndHospitalsModel(l, mu, n, N_lim, t_c)
    G = hospital.global_average_time_matrix()[:2,:,:]
    solution = np.min(G)
    if solution == 0:
        return 'Inconsistent'
    if G[0][0][0] == solution:
        return 'N2-AA'
    elif G[0][0][1] == solution:
        return 'N2-AR'
    elif G[0][1][0] == solution:
        return 'N2-RA'
    elif G[0][1][1] == solution:
        return 'N2-RR'
    elif G[1][0][0] == solution:
        return 'N1-AA'
    elif G[1][0][1] == solution:
        return 'N1-AR'
    elif G[1][1][0] == solution:
        return 'N1-RA'
    elif G[1][1][1]:
        return 'N1-RR'


def global_solution_plot(n, ax=None):
    print('Computing for n = {}'.format(n))
    data = {
        'Lambda': [],
        'Mu': [],
        'Optimal Strategy': []
    }
    for l in np.linspace(la_min, la_max, 30):
        for mu in np.linspace(mu_min, mu_max, 30):
            data['Lambda'].append(l)
            data['Mu'].append(mu)
            data['Optimal Strategy'].append(global_solution(l, mu, n))
    data = pd.DataFrame(data)
    sns.scatterplot(x='Lambda', y='Mu', hue='Optimal Strategy', data=data, palette=disp2str_palette, ax=ax, marker='s', s=1000)
    if ax is not None:
        ax.set_title('N = ' + str(n))


if __name__ == '__main__':
    sns.set(style='ticks')
    fig, axs = plt.subplots(ncols=3, nrows=3, figsize=(15, 15))
    global_solution_plot([1, 1], axs[0][0])
    global_solution_plot([1, 2], axs[0][1])
    global_solution_plot([1, 3], axs[0][2])
    global_solution_plot([2, 1], axs[1][0])
    global_solution_plot([2, 2], axs[1][1])
    global_solution_plot([2, 3], axs[1][2])
    global_solution_plot([3, 1], axs[2][0])
    global_solution_plot([3, 2], axs[2][1])
    global_solution_plot([3, 3], axs[2][2])
    fig.savefig('../../images/Dispatcher/Global Nash Equ')
    plt.show()
