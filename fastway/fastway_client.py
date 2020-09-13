from datetime import datetime, timedelta
from json import dump, dumps, load, loads
from os import system, name, path
from requests import get, post
from pandas import read_csv
from time import time

if name == "nt":
    SEP = "\\"
    CLEAR = "cls"
else:
    SEP = "/"
    CLEAR = "clear"

ROOT_DIR = path.dirname(path.abspath(__file__))
AUTH_DIR = SEP.join((ROOT_DIR, "auth"))
TRACK_DIR = SEP.join((ROOT_DIR, "track"))

AUTH_FILE = SEP.join((AUTH_DIR, "fastway_auth.json"))
TOKEN_FILE = SEP.join((AUTH_DIR, "fastway_token.json"))
LABELS_FILE = SEP.join((TRACK_DIR, "labels.csv"))

TOKEN_URL = "https://identity.fastway.org/connect/token"
TRACK_URL = "https://api.myfastway.com.au/api/track/label/"

def get_labels(file=LABELS_FILE):
    with open(file, "r") as file:
        results = read_csv(file, usecols=["Tracking Number"]).values.tolist()
        short_results = []
        for i in range(10):
            short_results.append(results[i])
        return short_results

def get_token(file=TOKEN_FILE):
    try:
        with open(file, "r") as file:
            token = load(file)
            if datetime.now().isoformat() < token["token_expiry"]:
                # print("Fetched with access token:", token["access_token"][-4:])
                credentials = (token["token_type"], token["access_token"])
                return { "Authorization": " ".join(credentials) }
            else:
                return renew_token()
    except FileNotFoundError:
        return renew_token()

def renew_token(files=(AUTH_FILE, TOKEN_FILE)):
    try:
        with open(files[0], "r") as file:
            authorization = load(file)
    except FileNotFoundError as exception:
        raise exception

    response = post(TOKEN_URL, data=authorization)

    token = loads(response.text)
    expiry = datetime.now() + timedelta(hours=1)
    token["token_expiry"] = expiry.isoformat()

    with open(files[1], "w") as file:
        dump(token, file, indent=4, sort_keys=True)

    print("Generated new access token:", token["access_token"][-4:])

    return get_token()

def track_items(labels=["BD0010915392"]):
    results = []
    for label in labels:
        response = get("".join((TRACK_URL, label)), headers=get_token())
        results.append(loads(response.text)["data"][-1])
    return results

def main():
    system(CLEAR)

    start = time()
    labels = get_labels()
    labels_str = []

    for label in labels:
        labels_str.append(label[0])

    response = track_items(labels_str)

    end = time()
    duration = end - start
    length = str(len(response))
    counter = 0

    for item in response:
        system(CLEAR)
        print(dumps(item, indent=4, sort_keys=True))
        print(" ".join(("Record", str(counter + 1), "of", length)))
        print(" ".join(("Fetched in", str(duration), "seconds.")))
        input("Press [ENTER] to continue: ")
        counter = counter + 1

    print("Done.")
    input("Press [ENTER] to exit: ")
    system(CLEAR)

if __name__ == "__main__":
    main()
