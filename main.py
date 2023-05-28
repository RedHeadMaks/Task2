import numpy as np

from sortedDict import *
from plotGraphic import *
from sarsa import *

def sarsa_():
    game = Game()
    num_episodes = 10 ** 4
    gamma = 0.5
    l = 0
    Q_mc, _, _ = monte_carlo_control(game, num_episodes, gamma)
    Q_sarsa, L_middle = sarsa(game, num_episodes, gamma, l)
    difference, difference_sum = getDifference(Q_sarsa, Q_mc)
    #plotGraphic(range(num_episodes), L_middle, "Номер эпизода", "Среднее значение ошибки")
    #plot_state_values(QtoV(difference))
    l = 1
    Q_sarsa, L_middle = sarsa(game, num_episodes, gamma, l)
    difference, difference_sum = getDifference(Q_sarsa, Q_mc)
    #plotGraphic(range(num_episodes), L_middle, "Номер эпизода", "Среднее значение ошибки")
    plot_state_values(QtoV(Q_sarsa))
    if True:
        return
    n = 11
    dif_array = np.ndarray(n, dtype=float)
    for p in range(n):
        Q_sarsa, L_middle = sarsa(game, num_episodes, gamma, p/n)
        difference, difference_sum = getDifference(Q_sarsa, Q_mc)
        #plotGraphic(range(num_episodes), L_middle, "Номер эпизода", "Среднее значение ошибки")
        #plot_state_values(QtoV(Q_sarsa))
        #L_summ[p] = sum(L_middle)
        dif_array[p] = difference_sum
    plotGraphic([x / 10.0 for x in range(n)], dif_array, "Лямбда", "Значение ошибки")

def monteCarlo():
    game = Game()
    num_episodes = 10 ** 5
    gamma = 1
    _, V, policy = monte_carlo_control(game, num_episodes, gamma)
    plot_state_values(V)

def main():
    #monteCarlo()
    sarsa_()

if __name__ == '__main__':
    main()