from gt.plot.DispatcherPlot import *


def find_nash(la, mu, n, print_matrix=False):
    model = DispatcherAndHospitalsModel(la, mu, n, 3, 10)
    matrix = model.game_matrix()
    if print_matrix:
        print(matrix)

    text = "NFG 1 R \"Ambulance Dispatching Game\" { \"Dispatcher\" \"Hospital1\" \"Hospital2\" }\n\n"
    text += "{ { \"N2\" \"N1\" }\n"
    text += "{ \"A\" \"R\" }\n"
    text += "{ \"A\" \"R\" }\n"
    text += "}\n\"\"\n\n"

    text += "{\n"
    for k in range(2):
        for j in range(2):
            for i in range(2):
                text += "{ \"\" %f, %f, %f }\n" % (matrix[i][j][k][0], matrix[i][j][k][1], matrix[i][j][k][2])
    text += "}\n"
    text += "1 2 3 4 5 6 7 8"

    game = Game(text)
    sol = game.findEquilibria()
    return sol


if __name__ == '__main__':
    la = 2
    mu = 2
    game = Game('2x2x2.nfg')
    print(game.findEquilibria('pne'))
    # print(find_nash(la, mu, [1,1], True))
    # la = 1.14414
    # model = HospitalsModel(la, mu, [1, 1], 3, 10)
    # print(model.global_average_time_matrix())
    # print(np.min(model.global_average_time_matrix()) >= 1e9)
