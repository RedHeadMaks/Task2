from BlackJack import *

def step(state: State, action: Action):
    game = Game(state)
    match action:
        case Action.hit:
            game.gamer_hit()
        case Action.stick:
            game.gamer_stick()
    return game.state, game.income