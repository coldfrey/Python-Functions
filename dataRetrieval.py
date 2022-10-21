import requests
import json

from CommerceQueries import addOrdersToDict
from getAuth import authToken


url = "https://uncommon.commercelayer.io/api/orders" #?page%5Bnumber%5D=14&page%5Bsize%5D=10"

payload={}
headers = {
  'Content-Type': 'application/vnd.api+json',
  'Authorization': 'Bearer ' + authToken
}

print('Running first api call...')
response = requests.request("GET", url, headers=headers, data=payload)
print('First api call success')
data = json.loads(response.text)

allOrders = {}
pageNumber = 0
    
while 1:
  urlDict = data['links']

  if pageNumber == 0:
    url = data['links']['last']
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    allOrders = addOrdersToDict(allOrders, data)
    pageNumber += 1

  elif 'prev' in urlDict.keys():
    # Request next page
    url = data['links']['prev']
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    allOrders = addOrdersToDict(allOrders, data)
    pageNumber += 1
  
  else:
    # Ran out of new pages
    print('Finished. Page count is: ' , str(pageNumber))
    pageNumber += 1
    break

# pendingOrders = allOrders['pending']
# print('\n Pending: \n')
# print(pendingOrders)
    
# draftOrders = allOrders['draft']
# print('\n Draft: \n')
# # print(draftOrders)

# placedOrders = allOrders['placed']
# print('\n Placed: \n')
# print(placedOrders)

with open("API_data.json", "w") as outfile:
    json.dump(allOrders, outfile, indent=4)


