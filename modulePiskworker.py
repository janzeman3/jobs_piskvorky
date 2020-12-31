import random

DELTA = 1

DIRECTION_SET = [{'x': 0, 'y': +1},
                 {'x': 0, 'y': -1},
                 {'x': +1, 'y': -1},
                 {'x': +1, 'y': 0},
                 {'x': +1, 'y': +1},
                 {'x': -1, 'y': -1},
                 {'x': -1, 'y': 0},
                 {'x': -1, 'y': +1}
                 ]


class Piskworker:
    userID = None
    opponentID = None
    coordinates = None

    # game range
    min_x = -28
    max_x = +28
    min_y = -20
    max_y = +20

    def __init__(self, user_id, opponent_id):
        self.userID = user_id
        self.opponentID = opponent_id

    def update_game_range(self):
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

    def update(self, game_status):
        self.coordinates = game_status["coordinates"]
        self.update_game_range()

    def is_empty(self, x, y):
        result = True
        for turn in self.coordinates:
            if turn['x'] == x and turn['y'] == y:
                result = False
                break
        return result

    def whos_is(self, x, y):
        result = None
        for turn in self.coordinates:
            if turn['x'] == x and turn['y'] == y:
                result = turn['playerId']
                break
        return result

    def get_score(self, x, y):
        score = 0
        for direction in DIRECTION_SET:
            if not self.is_empty(x+direction['x'], y+direction['y']):
                score += 1
                direction_id = self.whos_is(x+direction['x'], y+direction['y'])
                if self.whos_is(x + 2*direction['x'], y + 2*direction['y']) == direction_id:
                    score += 20
                    if self.whos_is(x + 3*direction['x'], y + 3*direction['y']) == direction_id:
                        score += 400
                        if self.whos_is(x + 4*direction['x'], y + 4*direction['y']) == direction_id:
                            score += 8000

        return score

    def get_a_guess(self):
        if len(self.coordinates) == 0:
            result_x = 0
            result_y = 0
        else:
            result_x = self.min_x
            result_y = self.min_y
        result_score = -1

        for x in range(self.min_x, self.max_x+1):
            for y in range(self.min_y, self.max_y + 1):
                if self.is_empty(x, y):
                    score = self.get_score(x, y)

                    if score > result_score or (score == result_score and random.random() > 0.5):
                        result_score = score
                        result_x = x
                        result_y = y

        return result_x, result_y
