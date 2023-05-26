import random

from BlackJack import *
from step import *
import numpy as np  # библиотека, используемая для вычислений с массивами
from collections import defaultdict  # библиотека, содержащая класс defaultdict

def createZeroDict():
    dict = {}
    for gamerValue in range(-10, 31):
        for dealerValue in range(-10, 31):
            state = State(gamerValue, dealerValue)
            dict[state] = np.zeros(2, dtype=float)
            state2 = State(gamerValue, dealerValue)
    return dict

def sortedDict(dict1):
    sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict
def monte_carlo_control(game: Game, num_episodes, gamma):
    # Создаем словарь, в котором будем хранить значение функции ценности состояний
    V = defaultdict(float)
    # Создаем словарь, в котором будем хранить значение функции Q-оценки
    Q = createZeroDict()
    # Создаем словарь, в котором будем считать, сколько раз мы посетили каждое состояние
    N = createZeroDict()
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

        if i < 5:
            for gamerValue in range(-10, 31):
                for dealerValue in range(-10, 31):
                    state = State(gamerValue, dealerValue)
                    if sum(N[state]) != 0:
                        print("N = ", N[state], sum(N[state]), state)

        # Генерируем эпизод до тех пор, пока не завершится
        while game.inGame:
            # if i < 100:
            #     N[state][0] += 1
            #     print("N = ", N[state], sum(N[state]))
            #     if sum(N[state]) != 0:
            #         print("N = ", N[state])
            E[state] = N0/(N0+np.sum(N[state]))
            if E[state] != 1:
                print("E = ", E[state])
            # print(state, state_value)
            # Агент выбирает действие
            action_index = np.random.choice([Action.hit, Action.stick]).value
            if np.random.random() < E[state]:
                action_index = np.argmax(Q[state])

            # print(action_index)
            action = Action(action_index)
            # print(action_index, action)
            # Совершаем действие и получаем награду и новое состояние
            next_state, reward = game.step(action)
            # Добавляем текущее состояние, действие и награду в эпизод
            episode.append((state, action_index, reward))
            # Переходим в новое состояние
            state = next_state

        # Определяем, какое значение награды мы получили в этом эпизоде
        G: float = 0.0
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]

            G = gamma * G + reward
            if state not in map(lambda elem: elem[0], episode[:t-1]):
                if i < 10:
                    print(action, N[state])
                # Прибавляем значение награды к Q-оценке
                N[state][action] += 1
                if i < 10:
                    print(N[state])
                added = (1 / N[state][action]) * (G - Q[state][action])
                Q[state][action] += added
                if action != np.argmax(Q[state]):
                    break

    # Получаем оптимальную стратегию из Q-оценки
    policy = {}
    for state, action_values in Q.items():
        policy[state] = np.argmax(action_values)

    # Получаем и возвращаем значение функции ценности состояний V
    for state, action_values in Q.items():
        V[state] = max(action_values)

    print(list(N.items())[0])
    for state, value in list(N.items()):
        if sum(value) > 10:
            # print(state, value)
            pass
    return V, policy

if __name__ == '__main__':
    game = Game()
    num_episodes = 10**4
    gamma = 1
    V, policy = monte_carlo_control(game, num_episodes, gamma)
    sortedV = list(sortedDict(V).items())
    print("\nV\n")

    for state, value in sortedV[:20]:
        print(state, value)
    for state, value in sortedV[-200:]:
        print(state, value)

    print("\npolicy\n")
    for state, action in list(policy.items())[:20]:
        print(state, Action(action))
    for state, action in list(policy.items())[-20:]:
        print(state, Action(action))