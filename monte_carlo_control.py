from Game import *
from generateEpisode import *
import numpy as np
from collections import defaultdict

def QtoV(Q):
    return {state: np.max(values) for state, values in Q.items()}

def QtoPolicy(Q):
    return {state: np.argmax(values) for state, values in Q.items()}

def monte_carlo_control(game: Game, num_episodes, gamma):
    # Создаем словарь, в котором будем хранить значение функции Q-оценки
    Q = createDefaultDict()
    # Создаем словарь, в котором будем считать, сколько раз мы посетили каждое состояние
    N = createDefaultDict()
    E = defaultdict(float)
    N0 = 100

    l = num_episodes // 10
    # Проходим по всем эпизодам
    for i in range(num_episodes):
        if i % l == 0:
            print(i*100 // num_episodes, "%")
        episode = generateEpisode(game, Q, E, N, N0)
        # Определяем, какое значение награды мы получили в этом эпизоде
        G: float = 0.0
        visited_state = set()
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]
            G = gamma * G + reward
            #if (state, action) not in visited_state:
            if state not in map(lambda elem: elem[0], episode[:t-1]):
                # Прибавляем значение награды к Q-оценке
                N[state][action] += 1
                added = (G - Q[state][action]) / N[state][action]
                Q[state][action] += added
                visited_state.add((state, action))

    # Получаем оптимальную стратегию из Q-оценки
    policy = QtoPolicy(Q)
    V = QtoV(Q)
    return Q, V, policy