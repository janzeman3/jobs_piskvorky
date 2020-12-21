import requests
import json

userRegistration = "https://piskvorky.jobs.cz/api/v1/user"
newUser = {'nickname': 'JanZeman3', 'email': 'janzeman3@gmail.cz'}

response = requests.post(userRegistration, data=json.dumps(newUser))
print("Kod:" + str(response.status_code))

print(response.json())

konec = input("Opiš si ID a bouchni do entru")
