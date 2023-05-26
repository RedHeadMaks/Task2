from Model import *

class Game:
    state: State
    inGame: bool
    income: int

    def __init__(self, state: State = State()):
        self.set(state)

    def reset(self):
        self.state = State()
        self.update()

    def set(self, state: State):
        self.state = state
        self.update()

    def update(self):
        self.inGame = False
        if (self.state.gamer < 0) or (self.state.gamer > 21):
            self.income = -1
        elif (self.state.dealer < 0) or (self.state.dealer > 21):
            self.income = 1
        elif self.state.dealer >= 17:
            if self.state.gamer > self.state.dealer:
                self.income = 1
            elif self.state.gamer < self.state.dealer:
                self.income = -1
            else:
                self.income = 0
        else:
            self.income = 0
            self.inGame = True

    def print(self):
        print(
            f"\nСтатистика игры\n"
            f"Очки игрока: {self.state.gamer}\n"
            f"Очки дилера: {self.state.dealer}\n"
            f"Игра продолжается: {self.inGame}\n"
            f"Доход: {self.income}"
        )

    def gamer_hit(self):
        # print(f"Выбрана карта: {card}")
        self.state.gamer += generateCard()
        self.update()

    def gamer_stick(self):
        while self.inGame:
            # print(f"Выбрана карта диллера: {card}")
            while self.state.dealer < 17 and self.state.dealer >= 0 and self.state.dealer <= 21:
                self.state.dealer += generateCard()
            self.update()

    def step(self, action: int):
        match action:
            case 0:
                self.gamer_hit()
            case 1:
                self.gamer_stick()
        return self.state, self.income