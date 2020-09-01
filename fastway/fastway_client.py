from os import system, name
import json, requests
""" from requests_oauthlib import OAuth2Session """


def clear_screen():
    if name == 'nt':
        system('cls')
    else: 
        system('clear')

def print_json(j):
    print(json.dumps(j, indent=4, sort_keys=True))

def print_request(r):
    print("HTTP Code", r.status_code)
    if r.text != "" and r.text != None:
        print_json(json.loads(r.text))
    else:
        print("No response.")


def read_token(file="fastway_token.json"):
    with open(file, "r") as file:
        return json.load(file)


def get_token(file="fastway_auth.json"):
    with open(file, "r") as file:
        auth = json.load(file)["oauth"]

    return requests.get(auth["authority"], headers=auth)


def track_item(token, label):
    url = "https://api.myfastway.com.au/api/track/label/"
    return requests.get(url + label, headers=token)


def main():
    clear_screen()

    label = input("Enter tracking number: ")
    result = track_item(get_token(), label)
    print_request(result)
    
    input("Press [ENTER] to exit.")
    clear_screen()


main()
