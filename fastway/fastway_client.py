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

def get_token():
    url = "https://identity.fastway.org/connect/token"

    grant_type = "{grant_type}"
    client_id = "{client_id}"
    client_secret = "{client_secret}"
    scope = "{scope}"

    auth = "?grant_type="+grant_type+"&client_id="+client_id+\
        "&client_secret="+client_secret+"&scope="+scope
    
    return r = requests.post(url + auth)

def track_item(token, label):
    url = "https://api.myfastway.com.au/api/track/label/"

    return r = requests.get(url + label)

def main():
    clear_screen()
    token = get_token()
    print_request(token)
    
    label = input("Enter tracking number: ")
    result = track_item(token, label)
    print_request(result)
    
    input("Press [ENTER] to exit.")
    clear_screen()

main()
