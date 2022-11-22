import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
authurl = "https://uncommon.commercelayer.io/oauth/token?"

payload = json.dumps({
  "grant_type": "client_credentials",
  "client_id": os.getenv('COMMERCE_LAYER_CLIENT_ID'),
  "client_secret": os.getenv('COMMERCE_LAYER_CLIENT_SECRET')
})

print(payload)

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

authResponse = requests.request("POST", authurl, headers=headers, data=payload)
print(authResponse.json())


authToken = json.loads(authResponse.text)['access_token']
print(authToken)
