from datetime import datetime, timedelta
from json import dump, load, loads
from os import system, name, path
from requests import get, post

ROOT_DIR = path.dirname(path.abspath(__file__))
AUTH_FILE = "/".join((ROOT_DIR, "fastway_auth.json"))
TOKEN_FILE = "/".join((ROOT_DIR, "fastway_token.json"))

def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else: 
        _ = system('clear')

def get_path(file):
    return "/".join((ROOT_DIR, file))

def get_authorization(file=AUTH_FILE):
    with open(file, "r") as file:
        return load(file)

def get_token(file=TOKEN_FILE):
    with open(file, "r") as file:
        return load(file)

def renew_token():
    url = "https://identity.fastway.org/connect/token"
    response = post(url, data=get_authorization())
    
    if 200 <= response <= 229:
        print("Succeeded with HTTP", response)
    else:
        print("Failed with HTTP", response)
    
    data = loads(response.text)
    expiry = datetime.now() + timedelta(hours=1)
    data["token_expiry"] = expiry.isoformat()

    with open(TOKEN_FILE, "w") as file:
        dump(data, file, indent=4, sort_keys=True)
    return response.status_code

def get_expiry(token=get_token()):
    return token["token_expiry"]

def get_header(token=get_token()):
    credentials = (token["token_type"], token["access_token"])
    return { "Authorization": " ".join(credentials) }

def track_item(label="BD0010915392"):
    url = "https://api.myfastway.com.au/api/track/label/"
    response = get("".join((url, label)), headers=get_header())
    return loads(response.text)["data"][-1]

def track_items(labels=("BD0010915392")):
    url = "https://api.myfastway.com.au/api/track/label/"
    results = []
    for label in labels:
        response = get("".join((url, label)), headers=get_header())
        results.append(loads(response.text)["data"][-1])
    return results

def main():
    input("Press [ENTER] to exit:")  
    clear_screen()

main()
