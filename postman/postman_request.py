import json, pprint, requests

def print_request(r):
    print("HTTP Code", r.status_code)
    if r.text != "" and r.text != None:
        data = json.loads(r.text)
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print("No response.")

label = input("Enter tracking number: ")

url = "https://api.myfastway.com.au/api/track/label/" + label

with open("../fastway/fastway_token",'r') as auth:
  headers = { "Authorization" : auth.readlines()[0] }

response = requests.request("GET", url, headers=headers)

print_request(response)
