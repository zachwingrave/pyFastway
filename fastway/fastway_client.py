from datetime import datetime, timedelta
from json import dump, dumps, load, loads
from os import system, name, path
from requests import get, post

if name == "nt":
    SEP = "\\"
    CLEAR = "cls"
else:
    SEP = "/"
    CLEAR = "clear"

ROOT_DIR = path.dirname(path.abspath(__file__))
AUTH_FILE = SEP.join((ROOT_DIR, "fastway_auth.json"))
TOKEN_FILE = SEP.join((ROOT_DIR, "fastway_token.json"))

def get_path(file):
    return SEP.join((ROOT_DIR, file))

def get_authorization(file=AUTH_FILE):
    try:
        with open(file, "r") as file:
            return load(file)
    except FileNotFoundError as exception:
        print(exception)
        return False

def get_token(file=TOKEN_FILE):
    try:
        with open(file, "r") as file:
            token = load(file)
            if datetime.now().isoformat() < token["token_expiry"]:
                return token
            else:
                return renew_token(file)
    except FileNotFoundError:
        return renew_token(file)

def renew_token(file=TOKEN_FILE):
    print("Generating new token...")
    url = "https://identity.fastway.org/connect/token"
    response = post(url, data=get_authorization())
    
    token = loads(response.text)
    expiry = datetime.now() + timedelta(hours=1)
    token["token_expiry"] = expiry.isoformat()

    with open(file, "w") as file:
        dump(token, file, indent=4, sort_keys=True)
    
    return token

def get_expiry(token=get_token()):
    if token:
        return token["token_expiry"]
    else:
        return False

def get_header(token=get_token()):
    if token:
        credentials = (token["token_type"], token["access_token"])
        return { "Authorization": " ".join(credentials) }
    else:
        return False

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
    response = track_item()
    
    print(dumps(response, indent=4, sort_keys=True))

    input("Press [ENTER] to exit:")  
    system(CLEAR)

main()
