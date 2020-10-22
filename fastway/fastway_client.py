from json import dump, dumps, load, loads
from datetime import datetime, timedelta
from os import system, name, path
import logging

from requests import get, post
from pandas import read_csv
from csv import writer

from time import time
from tqdm import tqdm
from sys import argv

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

# Root directory and log file constants.
ROOT_DIR = path.dirname(path.abspath(__file__))
LOG_FILE = SEP.join((ROOT_DIR, "log", "fastway.log"))

logging.basicConfig (
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)

# Directory constants for this project.
AUTH_DIR = SEP.join((ROOT_DIR, "auth"))
RESULTS_DIR = SEP.join((ROOT_DIR, "results"))
TRACKING_DIR = SEP.join((ROOT_DIR, "tracking"))

# Authentication file path constants for this project.
AUTH_FILE = SEP.join((AUTH_DIR, "fastway_auth.json"))
TOKEN_FILE = SEP.join((AUTH_DIR, "fastway_token.json"))

# Data file path constants for this project.
LABELS_FILE = SEP.join((TRACKING_DIR, "fastway_labels.csv"))
RESULTS_FILE = SEP.join((RESULTS_DIR, "fastway_results.csv"))

# Endpoint URLs for the myFastway API service.
TOKEN_URL = "https://identity.fastway.org/connect/token"
TRACKING_URL = "https://api.myfastway.com.au/api/track/label/"

def sort_keys(data):
    """Return key-sorted dict using JSON conversion."""
    return loads(dumps(data, sort_keys=True))

def get_labels(labels_file=LABELS_FILE):
    """Return tracking labels from spreadsheet as a list."""
    logging.info("Entering get_labels() function.")
    logging.info(":".join(("Opening file", labels_file)))
    with open(labels_file, "r") as file:
        data = read_csv(file, usecols=["Tracking Number"]).values.tolist()
    labels = []
    log_msg = "Getting labels from fastway_labels.csv"
    logging.info(log_msg)
    for label in data:
        labels.append(label[0])
    return labels

def get_token(token_file=TOKEN_FILE):
    """Return API bearer token for tracking endpoint as a header string."""
    logging.info("Entering get_token() function.")
    try:
        with open(token_file, "r") as file:
            token = load(file)
            if datetime.now().isoformat() < token["token_expiry"]:
                log_msg = " ".join(("Using existing access token:", token["access_token"][-4:]))
                logging.info(log_msg)
                print(log_msg)
                credentials = (token["token_type"], token["access_token"])
                return { "Authorization": " ".join(credentials) }
            else:
                return renew_token()
    except FileNotFoundError:
        return renew_token()

def renew_token(auth_file=AUTH_FILE, token_file=TOKEN_FILE):
    """Put new token in /auth/fastway_token.json and return get_token()."""
    logging.info("Entering renew_token() function.")
    try:
        with open(auth_file, "r") as file:
            authorization = load(file)
    except FileNotFoundError as exception:
        credentials = {
            "scope": "fw-fl2-api-au",
            "grant_type" : "client_credentials"
        }
        credentials["client_id"] = input("client_id: ")
        credentials["client_secret"] = input("client_secret: ")
        with open(auth_file, "w") as file:
            dump(credentials, file, indent=4)
        return renew_token()

    response = post(TOKEN_URL, data=authorization)

    token = loads(response.text)
    expiry = datetime.now() + timedelta(hours=1)
    token["token_expiry"] = expiry.isoformat()

    with open(token_file, "w") as file:
        dump(token, file, indent=4)

    log_msg = " ".join(("Generated new access token:", token["access_token"][-4:]))
    logging.info(log_msg)
    print(log_msg)

    return get_token()

def track_items(labels=["BD0010915392", "BD0010915414"]):
    """Return tracking API results for labels as a dict."""
    logging.info("Entering track_items() function.")
    start = time()
    results = []

    token = get_token()

    log_msg = "Getting API responses from fastway.org"
    logging.info(log_msg)
    print(log_msg)

    for label in tqdm(labels):
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
    logging.info("Entering print_reuslts() function.")
    counter = 0
    for item in response["results"]:
        system(CLEAR)
        counter = counter + 1
        print(dumps(item, indent=4, sort_keys=True))
        print(" ".join(("Fetched with access token:", response["token_id"])))
        print(" ".join(("Fetched in", str(response["duration"]), "seconds")))
        print(" ".join(("Record", str(counter), "of", response["records"])))
        option = input("Press [ENTER] to continue or type [q] to quit: ")
        if option.lower() == "q":
            break
    system(CLEAR)

def write_results(response, results_file=RESULTS_FILE):
    """Write tracking API results for labels into /tracking/results.csv."""
    logging.info("Entering write_results() function.")
    with open(results_file, "w", newline="") as file:
        csv_writer = writer(file)

        headers = response["results"][0].keys()
        csv_writer.writerow(headers)

        logging.info("Writing results to fastway_results.csv")

        for item in response["results"]:
            csv_writer.writerow(item.values())

def write_log(response):
    logging.info(" ".join(("Fetched at", str(response["datetime"]))))
    logging.info(" ".join(("Fetched", response["records"], "records")))
    logging.info(" ".join(("Fetched with access token:", response["token_id"])))
    logging.info(" ".join(("Fetched in", str(response["duration"]), "seconds")))

def write_log_json(response, log_file=LOG_FILE):
    logging.info("Entering write_log() function.")
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
    logging.info("Entering main() function.")
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
    logging.info("fastway_client.py has been called as main.")

    if len(argv) > 1:
        mode = argv[1]
        if mode not in ARGS:
            raise ValueError("Invalid argument '%s'" % mode)

        # loglevel = argv[2]
        # # assuming loglevel is bound to the string value obtained from the
        # # command line argument. Convert to upper case to allow the user to
        # # specify --log=DEBUG or --log=debug
        # numeric_level = getattr(logging, loglevel.upper(), None)
        # if not isinstance(numeric_level, int):
        #     raise ValueError('Invalid log level: %s' % loglevel)
        # logging.basicConfig(level=numeric_level, ...)

        main(mode)
    else:
        main()