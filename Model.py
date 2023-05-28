import random
from collections import defaultdict
import numpy as np
def generateCard():
    value = random.randint(1, 10)
    color = random.choice([-1, 1, 1])
    return value * color

class State:
    dealer: int
    gamer: int

    def __init__(self, gamer: int = None, dealer: int = None):
        if gamer is None or dealer is None:
            self.reset()
        else:
            self.gamer = gamer
            self.dealer = dealer

    def reset(self):
        dealer = generateCard()
        while dealer < 1:
            dealer = generateCard()

        gamer = generateCard()
        while gamer < 1:
            gamer = generateCard()

        self.dealer = dealer
        self.gamer = gamer

    def __eq__(self, other):
        return self.gamer == other.gamer and self.dealer == other.dealer

    def __hash__(self):
        return hash((self.gamer+11)*100 + self.dealer)

    def __str__(self):
        return f"(gamer: {self.gamer}, dealer: {self.dealer})"

def createDefaultDict():
    d = defaultdict(lambda: np.zeros(2))
    x_range = np.arange(0, 22)
    y_range = np.arange(0, 10)
    for y in y_range:
        for x in x_range:
            state = State(x, y)
            d[state] = np.zeros(2)
    return d

def getDifference(Q_sarsa: defaultdict, Q_mc: defaultdict):
    difference = createDefaultDict()
    keys = set()
    for state in difference.keys():
        keys.add(state)
    for state in keys:
        difference[state][0] = (Q_sarsa[state][0] - Q_mc[state][0]) ** 2
        difference[state][1] = (Q_sarsa[state][1] - Q_mc[state][1]) ** 2
    result = np.sum(list(difference.values()))
    return difference, result