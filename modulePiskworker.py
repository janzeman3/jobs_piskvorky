import random


class Piskworker:
    def __init__(self):
        pass

    def get_a_guess(self):
        x = random.randrange(-5, 5)
        y = random.randrange(-5, 5)
        return x, y
