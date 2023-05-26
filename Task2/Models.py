from enum import Enum

import numpy as np

from GenerateCard import *

class Action(Enum):
    hit = 0
    stick = 1

    def __str__(self):
        if self == self.stick:
            return "stick"
        else:
            return "hit"

class Result(Enum):
    win = 1
    loss = -1
    draw = 0

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

    def __lt__(self, other):
        if self.gamer < other.gamer:
            return True
        elif self.gamer > other.gamer:
            return False
        else:
            return self.dealer < other.dealer

    def __le__(self, other):
        if self.gamer < other.gamer:
            return True
        elif self.gamer > other.gamer:
            return False
        else:
            return self.dealer <= other.dealer

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return self.gamer == other.gamer and self.dealer == other.dealer

    def __hash__(self):
        return hash(100 + (self.gamer+10)*100 + self.dealer)

    def __str__(self):
        return f"(gamer: {self.gamer}, dealer: {self.dealer})"