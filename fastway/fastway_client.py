import json, pprint, requests
from os import system, name

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else: 
        _ = system('clear')

def get_token():
    pass

def track_item(label):
    url = "https://api.myfastway.com.au/api/track/label/"

    r = requests.get(url + label)

    print("HTTP Code", r.status_code)
    if r.text != "" and r.text != None:
        data = json.loads(r.text)
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print("No response.")

def main():
    clear()
    
    label = input("Enter tracking number: ")
    
    track_item(label)

    input("Press [ENTER] to exit.")

    clear()

main()
