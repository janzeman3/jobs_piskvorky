import requests
import json
from moduleUser import User


class PiskvorkyConnector:
    mainURL: str = "https://piskvorky.jobs.cz/api/"
    userRegistrationURL: str = mainURL + "v1/user"
    startGameURL: str = mainURL + "v1/connect"
    playURL: str = mainURL + "v1/play"
    checkURL: str = mainURL + "v1/checkStatus"
    checkLastURL: str = mainURL + "v1/checkLastStatus"

    def start_game(self):
        token = json.dumps({'userToken': User.Token})

        print("\nStarting a game...")
        response = requests.post(self.startGameURL, data=token)
        response_json = response.json()

        print("   Response code: " + str(response.status_code))
        print("   Response JSON: " + str(response_json))

        return response_json["gameToken"]

    def play(self, game_token, x, y):
        turn = json.dumps({ "userToken": User.Token,
                            "gameToken": game_token,
                            "positionX": x,
                            "positionY": y
                            })

        print("\nPlay on " + str(x) + "," + str(y))
        response = requests.post(self.playURL, data=turn)
        response_json = response.json()

        print("   Response code: " + str(response.status_code))
        print("   Response JSON: " + str(response_json))

        return response_json

    def check(self, game_token):
        print("\nGet game status")
        game =json.dumps({ "userToken": User.Token,
                           "gameToken": game_token
                            })

        response = requests.post(self.checkURL, data=game)
        response_json = response.json()

        print("  Response code: " + str(response.status_code))
        print("  Response JSON: " + str(response_json))

        return response_json

    def checkLast(self, game_token):
        print("\nGet last turn")
        game =json.dumps({ "userToken": User.Token,
                           "gameToken": game_token
                            })

        response = requests.post(self.checkLastURL, data=game)
        response_json = response.json()

        print("  Response code: " + str(response.status_code))
        print("  Response JSON: " + str(response_json))

        return response_json
