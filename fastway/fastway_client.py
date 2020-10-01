from json import dump, dumps, load, loads
from requests import get, post
from pandas import read_csv
from csv import writer

from datetime import datetime, timedelta
from os import system, name, path
from time import time
from sys import argv

from threading import Thread
from itertools import cycle

# OS variables.
if name == "nt":
    SEP = "\\"
    CLEAR = "cls"
else:
    SEP = "/"
    CLEAR = "clear"

# Command line arguments.
ARGS = [
    "write",
    "print"
]

# A noscan response.text is an empty list.
NOSCAN = []

# Directory file path constants for this project.
ROOT_DIR = path.dirname(path.abspath(__file__))
AUTH_DIR = SEP.join((ROOT_DIR, "auth"))
RESULTS_DIR = SEP.join((ROOT_DIR, "results"))
TRACKING_DIR = SEP.join((ROOT_DIR, "tracking"))

# Authentication file path constants for this project.
AUTH_FILE = SEP.join((AUTH_DIR, "fastway_auth.json"))
TOKEN_FILE = SEP.join((AUTH_DIR, "fastway_token.json"))

# Data file path constants for this project.
LOG_FILE = SEP.join((RESULTS_DIR, "log.json"))
LABELS_FILE = SEP.join((TRACKING_DIR, "labels.csv"))
RESULTS_FILE = SEP.join((RESULTS_DIR, "results.csv"))

# Endpoint URLs for the myFastway API service.
TOKEN_URL = "https://identity.fastway.org/connect/token"
TRACKING_URL = "https://api.myfastway.com.au/api/track/label/"

def sort_keys(data):
    """Return key-sorted dict using JSON conversion."""
    return loads(dumps(data, sort_keys=True))

def get_labels(labels_file=LABELS_FILE):
    """Return tracking labels from spreadsheet as a list."""
    with open(labels_file, "r") as file:
        data = read_csv(file, usecols=["Tracking Number"]).values.tolist()
    labels = []
    for label in data:
        labels.append(label[0])
    return labels

def get_token(token_file=TOKEN_FILE):
    """Return API bearer token for tracking endpoint as a header string."""
    try:
        with open(token_file, "r") as file:
            token = load(file)
            if datetime.now().isoformat() < token["token_expiry"]:
                credentials = (token["token_type"], token["access_token"])
                return { "Authorization": " ".join(credentials) }
            else:
                return renew_token()
    except FileNotFoundError:
        return renew_token()

def renew_token(auth_file=AUTH_FILE, token_file=TOKEN_FILE):
    """Put new token in /auth/fastway_token.json and return get_token()."""
    try:
        with open(auth_file, "r") as file:
            authorization = load(file)
    except FileNotFoundError as exception:
        raise exception

    response = post(TOKEN_URL, data=authorization)

    token = loads(response.text)
    expiry = datetime.now() + timedelta(hours=1)
    token["token_expiry"] = expiry.isoformat()

    with open(token_file, "w") as file:
        dump(token, file, indent=4, sort_keys=True)
    print("Generated new access token:", token["access_token"][-4:])
    return get_token()

def track_items(labels=["BD0010915392", "BD0010915414"]):
    """Return tracking API results for labels as a dict."""
    start = time()
    results = []

    token = get_token()

    for label in labels:
        response = get("".join((TRACKING_URL, label)), headers=token)
        response_data = loads(response.text)["data"]
        if response_data == NOSCAN:
            data = {
                "courierNo": None,
                "description": "This parcel was never scanned.",
                "franchiseCode": "UNK",
                "franchiseName": "Unknown",
                "labelNo": label,
                "scanType": "N",
                "scanTypeDescription": "No scan",
                "scannedDateTime": None,
                "status": "NSC"
            }
            response_data.append(data)
        results.append(sort_keys(response_data[-1]))

    curr_date = datetime.now().isoformat()
    token_id = token["Authorization"][-4:]
    duration = round(time() - start, 2)
    records = len(results)

    return {
        "results": results,
        "datetime": curr_date,
        "token_id": str(token_id),
        "duration": str(duration),
        "records": str(records),
    }

def print_results(response):
    """Print tracking API results to console for each label in response."""
    counter = 0
    for item in response["results"]:
        print(dumps(item, indent=4, sort_keys=True))
        print(" ".join(("Record", str(counter + 1), "of", response["records"])))
        print(" ".join(("Fetched with access token:", response["token_id"])))
        print(" ".join(("Fetched in", str(response["duration"]), "seconds")))
        input("Press [ENTER] to continue: ")
        counter = counter + 1
        system(CLEAR)

def write_results(response, results_file=RESULTS_FILE):
    """Write tracking API results for labels into /tracking/results.csv."""
    with open(results_file, "w", newline="") as file:
        csv_writer = writer(file)

        headers = response["results"][0].keys()
        csv_writer.writerow(headers)

        for item in response["results"]:
            csv_writer.writerow(item.values())

def write_log(response, log_file=LOG_FILE):
    """Write tracking API results metadata into /results/log.json."""
    try:
        with open(log_file, "r") as file:
            log = load(file)
    except FileNotFoundError as exception:
        log = {
            "data": []
        }

    response.pop("results", None)
    response["records"] = " ".join(("Fetched", response["records"], "records"))
    response["token_id"] = " ".join(("Fetched with access token:", response["token_id"]))
    response["duration"] = " ".join(("Fetched in", str(response["duration"]), "seconds"))

    log["data"].append(response)
    with open(log_file, "w") as file:
        dump(log, file, indent=4)

def main(mode="write"):
    """Main function of the program."""
    system(CLEAR)

    labels = get_labels()
    response = track_items(labels)

    if mode == "write":
        write_results(response)
    elif mode == "print":
        print_results(response)

    write_log(response)

    system(CLEAR)

# Execute the main function.
if __name__ == "__main__":

    if len(argv) > 1:
        mode = argv[1]
        if mode not in ARGS:
            raise ValueError("Invalid argument '%s'" % mode)
        main(mode)
    else:
        main()