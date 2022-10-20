import requests
import json


authurl = "https://uncommon.commercelayer.io/oauth/token?"

payload = json.dumps({
  "grant_type": "client_credentials",
  "client_id": "REPLACE_WITH_CLIENT_ID",
  "client_secret": "REPLACE WITH SECRET"
})

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

authresponse = requests.request("POST", authurl, headers=headers, data=payload)
authToken = json.loads(authresponse.text)['access_token']
