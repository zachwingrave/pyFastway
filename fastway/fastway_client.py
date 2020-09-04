from os import system, name, path, getcwd
from datetime import datetime, timedelta
import json, requests

file = "fastway_auth.json"
with open(file, "r") as file:
    authorization = json.load(file)

def clear_screen():
    if name == 'nt':
        system('cls')
    else: 
        system('clear')

def get_token(authorization):
    url = "https://identity.fastway.org/connect/token"
    response = requests.post(url, data=authorization)

    data = json.loads(response.text)
    expiry = (datetime.now() + timedelta(hours=1)).isoformat()
    data["expiry_date"] = expiry

    print(json.dumps(data, indent=4, sort_keys=True))
    with open("fastway_token.json", "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)
    return response.status_code

def get_token_expiry(token):
    pass

def get_token_header(token):
    return { "Authorization": token["token_type"] + " " + token["access_token"] }

def track_item(token_header, label):
    url = "https://api.myfastway.com.au/api/track/label/"
    return requests.get(url + label, headers=token_header)

def track_one_item():
    clear_screen()
    
    token = json.loads(get_token(authorization))
    token_header = get_token_header(token)

    label = input("Enter tracking number: ")
    response = track_item(token_header, label)

    print("HTTP Code", response.status_code)
    if response.text != "" and response.text != None:
        print(response.json())
        #print(json.dumps(response.text, indent=4, sort_keys=True))
        #print_json(json.loads(response.text))
    else:
        print("No response.")

    input("Press [ENTER] to exit.")
    clear_screen()

def main():
    clear_screen()
    
    print("Generating token into fastway_token.json...")

    response = get_token(authorization)

    if 200 <= response <= 229:
        print("Succeeded with HTTP", response)
    else:
        print("Failed with HTTP", response)

    input("Press [ENTER] to exit.")
    clear_screen()

def get_path():
    print(getcwd())
    print(path.abspath(getcwd()))

get_path()
