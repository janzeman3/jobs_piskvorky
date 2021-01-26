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

COEF_QUEUE = 15
COEF_EMPTY_END = 2


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
        if user_id == opponent_id:
            print('Error!!!')
            quit()
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

    def whos_is(self, x, y, direction=None, distance=0):
        if direction is None:
            direction = {'x': 0, 'y': 0}

        result = None
        final_x = x + direction['x']*distance
        final_y = y + direction['y']*distance
        for turn in self.coordinates:
            if turn['x'] == final_x and turn['y'] == final_y:
                result = turn['playerId']
                break
        return result

    def is_potential_here(self, x, y, direction, player_id):
        distance_positive = 1
        potential = 1
        while self.whos_is(x, y, direction, distance_positive) in [player_id, None] and distance_positive <= 5:
            distance_positive += 1
            potential += 1

        distance_negative = 1
        while self.whos_is(x, y, direction, -distance_negative) in [player_id, None] and distance_negative <= 5:
            distance_negative += 1
            potential += 1

        if potential >= 5:
            return True
        else:
            return False

    def get_direction_score_one_way(self, x, y, direction, player_id, step):
        direction_score = 1
        distance = step
        space_count = 0
        while self.whos_is(x, y, direction, distance) in [player_id, None] and abs(distance) < 5:
            if self.whos_is(x, y, direction, distance) == player_id:
                direction_score *= (COEF_QUEUE - space_count)
                space_count = 0
            elif self.whos_is(x, y, direction, distance) is None:
                space_count += 1
            distance += step
        if abs(distance) >= 5:
            direction_score *= COEF_EMPTY_END
        return direction_score

    # returns score of the position according to direction
    def get_direction_score(self, x, y, direction, player_id):
        direction_score = 1
        if self.is_potential_here(x, y, direction, player_id):
            direction_score *= self.get_direction_score_one_way(x, y, direction, player_id, +1)
            direction_score *= self.get_direction_score_one_way(x, y, direction, player_id, -1)

        print("..." + str(direction) + " " + str(direction_score) + " " + player_id)
        return direction_score

    # Returns score of the position on the board.
    def get_score(self, x, y):
        print(str(x) + ", " + str(y) + "Starting...")
        offense_score = 0
        defense_score = 0
        for direction in DIRECTION_SET:
            offense_score += self.get_direction_score(x, y, direction, self.userID)
            defense_score += self.get_direction_score(x, y, direction, self.opponentID)

        score = offense_score + defense_score
        print(str(x) + ", " + str(y) + ": score " + str(offense_score) + " + " + str(defense_score))

        return score

    # Goes over all position on the board and get the score. Then chooses the best score and returns it.
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
