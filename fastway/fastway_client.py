from os import system, name
from time import time
import json, requests

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

def get_token(authorization):
    url = "https://identity.fastway.org/connect/token"
    return requests.post(url, data=authorization).text

def get_token_header(j):
    return { "Authorization": j["token_type"] + " " + j["access_token"] }

def track_item(token_header, label):
    url = "https://api.myfastway.com.au/api/track/label/"
    return requests.get(url + label, headers=token_header)

def main():
    file = "fastway_auth.json"
    with open(file, "r") as file:
        authorization = json.load(file)

    clear_screen()
    
    token = json.loads(get_token(authorization))
    token_header = get_token_header(token)
    
    label = input("Enter tracking number: ")
    start = time()
    result = track_item(token_header, label)
    print_request(result)

    end = time()
    print("Took", end-start, "seconds to fetch.")

    input("Press [ENTER] to exit.")
    
    clear_screen()

main()