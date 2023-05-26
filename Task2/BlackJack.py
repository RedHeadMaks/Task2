from Models import *

class Game:
    state: State
    result: Result
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
        self.inGame = True
        self.result = Result.draw

        if (self.state.gamer < 0) or (self.state.gamer > 21) or self.state.dealer == 21:
            self.result = Result.loss
            self.inGame = False
        elif (self.state.dealer < 0) or (self.state.dealer > 21) or self.state.gamer == 21:
            self.result = Result.win
            self.inGame = False
        elif self.state.dealer >= 17:
            if self.state.gamer > self.state.dealer:
                self.result = Result.win
            elif self.state.gamer < self.state.dealer:
                self.result = Result.loss
            else:
                self.result = Result.draw
            self.inGame = False

        if self.inGame:
            self.income = 0
        else:
            self.income = self.result.value

    def print(self):
        print(
            f"\nСтатистика игры\n"
            f"Очки игрока: {self.state.gamer}\n"
            f"Очки дилера: {self.state.dealer}\n"
            f"Игра продолжается: {self.inGame}\n"
            f"Доход: {self.income}"
        )

    def gamer_hit(self):
        card = generateCard()
        # print(f"Выбрана карта: {card}")
        self.state.gamer += card
        self.update()

    def gamer_stick(self):
        while self.inGame:
            card = generateCard()
            # print(f"Выбрана карта диллера: {card}")
            self.state.dealer += card
            self.update()

    def step(self, action: Action):
        match action:
            case Action.hit:
                self.gamer_hit()
            case Action.stick:
                self.gamer_stick()
        return self.state, self.income

if __name__ == '__main__':
    black = 0
    red = 0
    action = Action.hit
    result = Result.win

    game = Game()
    game.print()
    while game.inGame:
        if game.state.gamer < 18:
            game.gamer_hit()
        else:
            game.gamer_stick()
        game.print()

