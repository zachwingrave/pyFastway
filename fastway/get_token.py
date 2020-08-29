from fastway_utils import requests, read_token

def get_token():
    url = "https://identity.fastway.org/connect/token"

    headers = {
        "grant_type" : "{grant_type}",
        "client_id" : "{client_id}",
        "client_secret" : "{client_secret}",
        "scope" : "{scope}"
    }

    return requests.post(url, headers=headers)

read_token()