import random
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