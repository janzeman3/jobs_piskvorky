from moduleUser import User
from modulePiskvorkyJobs import PiskvorkyConnector
from time import sleep
import random

TIMESTEP = 10

def wait_for_opponent():
    opponent = None
    while not opponent:
        statusJSON = server.check(gameToken)
        sleep(TIMESTEP)
        opponent = statusJSON['playerCircleId']

print("User ID:    " + User.ID)
print("User Token: " + User.Token)

server = PiskvorkyConnector()

print("Starting game")
gameToken = server.start_game()

server.check(gameToken)

wait_for_opponent()

print("\nTry to play")

x = random.randrange(-28,28)
y = random.randrange(-20,20)

error_code = 0
while error_code != 226:
    # send the turn
    turn_JSON = server.play(gameToken, x, y)
    error_code = turn_JSON["statusCode"]

    # position is occupied
    if error_code == 409:
        x = random.randrange(-5, 5)
        y = random.randrange(-5, 5)

    print("\nCheck game")
    server.check(gameToken)
    print("\nCheck last")
    server.check(gameToken)

    sleep(3)
