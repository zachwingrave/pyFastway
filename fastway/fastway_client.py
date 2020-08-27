from fastway_utils import requests, clear_screen, print_request

def get_token():
    url = "https://identity.fastway.org/connect/token"

    headers = {
        "grant_type" : "{grant_type}",
        "client_id" : "{client_id}",
        "client_secret" : "{client_secret}",
        "scope" : "{scope}"
    }

    return requests.post(url, headers=headers)

def track_item(token, label):
    url = "https://api.myfastway.com.au/api/track/label/"
    
    with open("fastway_token",'r') as auth:
        headers = { "Authorization" : auth.readlines()[0] }

    return requests.get(url + label, headers=headers)

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
