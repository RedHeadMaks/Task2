from Game import *
import numpy as np
from collections import defaultdict
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def monte_carlo_control(game: Game, num_episodes, gamma):
    # Создаем словарь, в котором будем хранить значение функции ценности состояний
    V = defaultdict(float)
    # Создаем словарь, в котором будем хранить значение функции Q-оценки
    Q = defaultdict(lambda: np.zeros(2))
    # Создаем словарь, в котором будем считать, сколько раз мы посетили каждое состояние
    N = defaultdict(lambda: np.zeros(2))
    E = defaultdict(float)
    N0 = 100

    l = num_episodes//100
    # Проходим по всем эпизодам
    for i in range(num_episodes):
        if i % l == 0:
            print(i*100 // num_episodes, "%")
        episode = []  # создаем пустой список для хранения эпизода
        game.reset()  # возвращаем среду в начальное состояние
        state = game.state

        # Генерируем эпизод до тех пор, пока не завершится
        while game.inGame:
            E[state] = N0/(N0+np.sum(N[state]))
            if E[state] != 1:
                print("E = ", E[state])
            # print(state, state_value)
            # Агент выбирает действие
            action = np.argmax(Q[state])
            if np.random.random() < E[state]:
                action = np.random.choice([0, 1])
            # Совершаем действие и получаем награду и новое состояние
            next_state, reward = game.step(action)
            # Добавляем текущее состояние, действие и награду в эпизод
            episode.append((state, action, reward))
            # Переходим в новое состояние
            state = next_state

        # Определяем, какое значение награды мы получили в этом эпизоде
        G: float = 0.0
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]

            G = gamma * G + reward
            if state not in map(lambda elem: elem[0], episode[:t-1]):
                # Прибавляем значение награды к Q-оценке
                N[state][action] += 1
                added = (G - Q[state][action]) / N[state][action]
                if (Q[state][action]) > 0 and G > 1:
                    print("G ", G, " Add ", added, "Q[state][action] ", Q[state][action])
                Q[state][action] += added
                if action != np.argmax(Q[state]):
                    break

    # Получаем оптимальную стратегию из Q-оценки
    policy = {}
    for state, action_values in Q.items():
        policy[state] = np.argmax(action_values)

    # Получаем и возвращаем значение функции ценности состояний V
    for state, action_values in Q.items():
        V[state] = np.max(action_values)
    return V, policy

def sortedDict(dict1):
    sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict

def plot_linear_3d_from_dict(data_dict: dict):
    x = []
    y = []
    z = []
    value = []
    for key, val in data_dict.items():
        # Разбиваем значения в ключе на координаты
        x.append(key.gamer)
        y.append(key.dealer)
        z.append(val)
        value.append(val)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)

    ax.set_xlabel('gamer')
    ax.set_ylabel('dealer')
    ax.set_zlabel('Value')

    plt.show()
def plot_3d_from_dict(data_dict: dict):
    sorted_items = sorted(data_dict.items(), key=lambda x: (x[0].dealer, x[0].gamer))
    state_values = np.array([([item[0].gamer, item[0].dealer, item[1]]) for item in sorted_items])
    x, y, z = state_values[:, 0], state_values[:, 1], state_values[:, 2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.set_xlabel('gamer')
    ax.set_ylabel('dealer')
    ax.set_zlabel('Value')
    plt.show()



if __name__ == '__main__':
    game = Game()
    num_episodes = 10**5
    gamma = 1
    V, policy = monte_carlo_control(game, num_episodes, gamma)
    sortedV = list(sortedDict(V).items())
    print("\nV\n")

    for state, value in sortedV[:20]:
        print(state, value)
    for state, value in sortedV[-20:]:
        print(state, value)

    print("\npolicy\n")
    for state, action in list(policy.items())[:20]:
        print(state, action)
    for state, action in list(policy.items())[-20:]:
        print(state, action)

    plot_3d_from_dict(V)