import random
from enum import Enum

class Color(Enum):
    red = -1
    black = 1

def generateCard():
    random.seed()
    value = random.randint(1, 10)
    color = random.choice([Color.red, Color.black, Color.black]).value
    return value * color

if __name__ == '__main__':
    black = 0
    red = 0
    for i in range(100):
        value = generateCard()
        if value > 0:
            black += value
        else:
            red += value
    print(red, black)
