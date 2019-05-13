from gt.plot.DispatcherPlot import *
from gt.core.HospitalsModel import HospitalsModel
from gt.plot.HospitalNashPlot import *

if __name__ == '__main__':
    la = 1.14414
    mu = 0.01
    model = HospitalsModel(la, mu, [1, 1], 3, 10)
    print(model.global_average_time_matrix())
    # la = 1.14414
    # model = HospitalsModel(la, mu, [1, 1], 3, 10)
    # print(model.global_average_time_matrix())
    # print(np.min(model.global_average_time_matrix()) >= 1e9)
