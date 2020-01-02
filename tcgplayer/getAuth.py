import json, requests

client_Id = "84F0847D-8800-49D9-BA64-C35E978F672C"
client_Secret = "5E3B4EBB-0E06-4CE3-993C-D3318A8310FB"

payload = {
    'client_id': client_Id,
    'client_secret': client_Secret,
    "grant_type": "client_credentials"
}

url = "http://api.tcgplayer.com/token"
url1 = "http://api.tcgplayer.com/catalog/products?groupId=ELD"

r = requests.post(url,
    headers={"Content-Type":"application/json"},
    data=payload)

body = json.loads(r.content)
print(body)

with open('token.json', 'w', encoding='utf-8') as f:
    json.dump(body, f, ensure_ascii=False, indent=4)