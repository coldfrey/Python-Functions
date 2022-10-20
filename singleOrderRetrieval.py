import requests
import json

url = "https://uncommon.commercelayer.io/api/orders"

payload={}
headers = {
  'Content-Type': 'application/vnd.api+json',
  'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb24iOnsiaWQiOiJ3UlBwRUZ2TFFSIiwic2x1ZyI6InVuY29tbW9uIiwiZW50ZXJwcmlzZSI6ZmFsc2V9LCJhcHBsaWNhdGlvbiI6eyJpZCI6ImRNbldtaUx5WnAiLCJraW5kIjoiaW50ZWdyYXRpb24iLCJwdWJsaWMiOmZhbHNlfSwidGVzdCI6dHJ1ZSwiZXhwIjoxNjk0MjA1MTgyLCJyYW5kIjowLjEyOTI4OTU1Mzk0OTcyMjd9.yoNzjoYE-Y6F6ZFltfRWACuQwcE7ihP4oS00-uOk70WkARnX87JFSBjBKmwyR2qTeZ6BqTfQEBJ7eedOOwbSNA'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


data = json.loads(response.text)

# allOrders = {}
# for order in data['data']:

#     orderInfo = {}
#     attributes = order['attributes']
#     orderID = attributes['number']

#     orderInfo['OrderDate'] = attributes['payment_updated_at']

data = json.loads(response.text)

# allOrders = {}
# for order in data['data']:

#     orderInfo = {}
#     attributes = order['attributes']
#     orderID = attributes['number']

#     orderInfo['OrderDate'] = attributes['payment_updated_at']
