import random

DELTA = 1

class Piskworker:
    userID = None
    opponentID = None
    coordinates = None

    # game range
    min_x = -28
    max_x = +28
    min_y = -20
    max_y = +20

    def __init__(self, UserID, opponentID):
        self.userID = UserID
        self.opponentID = opponentID

    def update_gamerange(self):
        min_x = 28
        max_x = -28
        min_y = 20
        max_y = -20

        for turn in self.coordinates:
            x = turn["x"]
            y = turn["y"]

            min_x = min(x-DELTA, min_x)
            max_x = max(x+DELTA, max_x)
            min_y = min(y-DELTA, min_y)
            max_y = max(y+DELTA, max_y)

        self.min_x = max(min_x, -28)
        self.max_x = min(max_x, +28)
        self.min_y = max(min_y, -20)
        self.max_y = min(max_y, +20)

        print("Min X" + str(min_x))
        print("Max X" + str(max_x))
        print("Min Y" + str(min_y))
        print("Min Y" + str(max_y))

    def update(self, gameStatus):
        self.coordinates = gameStatus["coordinates"]
        self.update_gamerange()

    def get_a_guess(self):
        x = random.randrange(self.min_x, self.max_x)
        y = random.randrange(self.min_y, self.max_y)
        return x, y
