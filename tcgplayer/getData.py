import json, requests

client_Id = "84F0847D-8800-49D9-BA64-C35E978F672C"
client_Secret = "5E3B4EBB-0E06-4CE3-993C-D3318A8310FB"

with open('token.json') as token_file:
    token_data = json.load(token_file) 

bearer = token_data['token_type']
bearer_token = token_data['access_token']

combine = bearer + " " + bearer_token

root_url = "http://api.tcgplayer.com/v1.36.0"
url_temp = "/catalog/categories/1/groups/"

yeet = {
    "Accept":"application/json",
    "Authorization": combine
}

def getGroups():
    r = requests.get(root_url + url_temp,
        headers=yeet,
        params={"limit": '253'})

    body = json.loads(r.content)

    with open('sets.json', 'w', encoding='utf-8') as f:
        json.dump(body, f, ensure_ascii=False, indent=4)

def getCardPrice():
    url = "http://api.tcgplayer.com/v1.32.0/pricing/product/188630"
    response = requests.get(url, headers=yeet)
    body = json.loads(response.content)
    print(body)

getCardPrice()