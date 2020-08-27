import json, pprint, requests
from os import system, name

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else: 
        _ = system('clear')

def print_request(r):
    print("HTTP Code", r.status_code)
    if r.text != "" and r.text != None:
        data = json.loads(r.text)
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print("No response.")
