from moduleUser import User
from modulePiskvorkyJobs import PiskvorkyConnector
from time import sleep
from modulePiskworker import Piskworker

TIMESTEP_OPPONENT_WAIT = 1
TIMESTEP_OPPONENT_PLAY = 1

def wait_for_opponent(myID):
    opponentID = None
    while not opponentID:
        statusJSON = server.check(gameToken)
        sleep(TIMESTEP_OPPONENT_WAIT)
        if statusJSON['playerCircleId'] == myID:
            opponentID = statusJSON['playerCrossId']
        else:
            opponentID = statusJSON['playerCircleId']
    return opponentID


def wait_for_turn():
    print("Waiting for our turn...")
    while server.checkLast(gameToken, False)["actualPlayerId"] != User.ID:
        sleep(TIMESTEP_OPPONENT_PLAY)


print("User ID:    " + User.ID)
print("User Token: " + User.Token)

server = PiskvorkyConnector()

print("Starting game")
gameToken = server.start_game()
opponentID = wait_for_opponent(User.ID)
logic = Piskworker(User.ID, opponentID)

error_code = 0
while error_code != 226:
    wait_for_turn()

    # update statistics
    gameStatus = server.check(gameToken)
    logic.update(gameStatus)

    # generate turn
    x, y = logic.get_a_guess()

    # send the turn
    turn_JSON = server.play(gameToken, x, y)
    error_code = turn_JSON["statusCode"]

    # position is occupied
    if error_code == 409:
        # update statistics
        pass
        # and generate new turn
        x, y = logic.get_a_guess()

    if error_code == 406:
        print("Error: waiting for my turn does not work!!!")

    sleep(TIMESTEP_OPPONENT_PLAY)
