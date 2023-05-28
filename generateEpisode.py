import copy

import numpy as np

def generateEpisode(game, Q, E, N, N0):
    episode = []  # создаем пустой список для хранения эпизода
    game.reset()  # возвращаем среду в начальное состояние
    state = copy.copy(game.state)
    while game.inGame:
        E[state] = N0 / (N0 + np.sum(N[state]))
        # print(state, state_value)
        # Агент выбирает действие
        action = np.argmax(Q[state])
        if np.random.random() <= E[state]:
            action = np.random.choice([0, 1])
        # Совершаем действие и получаем награду и новое состояние
        next_state, reward = game.step(action)
        # Добавляем текущее состояние, действие и награду в эпизод
        episode.append((state, action, reward))
        # Переходим в новое состояние
        state = copy.copy(next_state)
    return episode