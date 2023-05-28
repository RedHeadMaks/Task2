from monte_carlo_control import *

def QSum(Q: defaultdict):
    np.sum(Q.values())
def sarsa(game: Game, num_episodes, gamma, lamda):
    Q_sarsa = createDefaultDict()
    N_sarsa = createDefaultDict()
    E = defaultdict(float)
    N0 = 100
    L_middle = np.ndarray(num_episodes)

    l = num_episodes//10
    # Проходим по всем эпизодам
    for i in range(num_episodes):
        if i % l == 0:
            print(i*100 // num_episodes, "%")
        episode = generateEpisode(game, Q_sarsa, E, N_sarsa, N0)
        L_sarsa = defaultdict(lambda: np.zeros(2))
        for t in range(len(episode)-1):
            state, action, reward = episode[t]
            state2, action2, reward2 = episode[t+1]
            L_sarsa[state][action2] += 1
            N_sarsa[state][action] += 1
            b = reward2 + gamma*Q_sarsa[state2][action2] - Q_sarsa[state][action]
            added = (b*L_sarsa[state][action])/N_sarsa[state][action]
            Q_sarsa[state][action] += added
            L_sarsa[state][action] *= lamda*gamma
        #print(np.sum(list(L_sarsa.values())))
        L_middle[i] = np.sum(list(L_sarsa.values())) #/ len(L_sarsa)

    return Q_sarsa, L_middle