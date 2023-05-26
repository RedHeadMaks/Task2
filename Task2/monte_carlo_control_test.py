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

def make_epsilon_greedy_policy(Q,epsilon,nA):
    """
         Создать эпсилон жадную стратегию, основанную на заданной функции значения Q и эпсилоне
         Параметры:
                 Q: Словарь, который отображает состояния в функции значений действия. Каждое значение представляет собой массив размером nA.
                 эпсилон: вероятность выбора случайного действия, число с плавающей запятой от 0 до 1.
                 nA: количество действий в среде.
         возвращаемое значение:
                 Возвращает функцию, входом которой является наблюдение или состояние, и возвращает вероятность каждого действия в виде массива с нулевыми значениями (длина nA).
    """
    def policy_fn(obseration):
        A=np.ones(nA,dtype=float)*epsilon/nA
        best_action=np.argmax(Q[obseration])
        A[best_action]+=(1.0-epsilon)
        return A
    return policy_fn
def mc_control_epsilon_greedy(env, num_episodes, discount_factor=1.0, epsilon=0.1):
    """
         Используйте жадную стратегию эпсилон для контроля Монте-Карло, чтобы найти лучшую жадную стратегию эпсилон.
         Параметры:
                 env: среда для занятий спортом OpenAI.
                 num_eposides: выборочная алгебра.
                 discount_factor: коэффициент дисконтирования гаммы.
                 эпсилон: вероятность выбора случайного действия, число с плавающей запятой от 0 до 1.
         возвращаемое значение:
                 Возврат кортежа (Q, policy). Q - это словарь, который отображает состояние в функцию значения действия, policy - это функция, которая принимает наблюдение в качестве входных данных и возвращает вероятность действия
    """
    # Отслеживать время и возврат каждого состояния для расчета среднего, вы можете использовать массив, чтобы сохранить все
    # Возврат (как показано в книге), но это неэффективно с памятью.
    returns_sum = defaultdict(float)
    returns_count = defaultdict(float)

    # Final action value function
    # Это вложенный словарь, отображающий состояние на (действие -> значение действия)
    Q = defaultdict(lambda: np.zeros(2))

    # Следуйте стратегии
    policy = make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)

    for i_episode in range(1, num_episodes + 1):
        # Печать текущего поколения для отладки
        if i_episode % 1000 == 0:
            print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
            sys.stdout.flush()
        # Генерация образцов данных
        # Generation - последовательность массивов, состоящая из кортежа (состояние, действие, награда)
        episode = []
        # Сброс, чтобы получить начальное состояние
        state = env.reset()
        for t in range(100):
            probs = policy(state)
            action = np.random.choice(np.arange(len(probs)), p=probs)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state

        # Найти все посещенные пары состояние-действие в текущем поколении
        # Преобразуйте каждое состояние в кортеж для использования в качестве словаря (удаляйте дублирующиеся элементы через set)
        sa_in_episode = set([(tuple(x[0]), x[1]) for x in episode])
        for state, action in sa_in_episode:
            sa_pair = (state, action)
            # Найти позицию, где пара состояние-действие (состояние, действие) впервые появляется в текущем поколении
            first_occurence_idx = next(i for i, x in enumerate(episode) if x[0] == state and x[1] == action)
            # Суммируйте все награды с первого появления
            G = sum([x[2] * (discount_factor ** i) for i, x in enumerate(episode[first_occurence_idx:])])
            # Рассчитать среднюю доходность состояния по всем алгебрам выборки
            returns_sum[sa_pair] += G
            returns_count[sa_pair] += 1.0
            Q[state][action] = returns_sum[sa_pair] / returns_count[sa_pair]

            # Изменяя словарь Q, стратегия может быть неявно улучшена
    return Q, policy

def sortedDict(dict1):
    sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict

if __name__ == '__main__':
    game = Game()
    num_episodes = 10**4
    gamma = 1
    V, policy = mc_control_epsilon_greedy(game, num_episodes, gamma)
    sortedV = list(sortedDict(V).items())
    print("\nV\n")

    for state, value in sortedV[:20]:
        print(state, value)
    for state, value in sortedV[-20:]:
        print(state, value)

    print("\npolicy\n")
    for state, action in list(policy.items())[:20]:
        print(state, Action(action))
    for state, action in list(policy.items())[-20:]:
        print(state, Action(action))