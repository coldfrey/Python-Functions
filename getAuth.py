import requests
import json
import os

authurl = "https://uncommon.commercelayer.io/oauth/token?"

payload = json.dumps({
  "grant_type": "client_credentials",
  # "client_id": os.environ["REPLACE_WITH_CLIENT_ID"],
  # "client_secret": os.environ["REPLACE_WITH_SECRET"]
})

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

authresponse = requests.request("POST", authurl, headers=headers, data=payload)
authToken = json.loads(authresponse.text)['access_token']
