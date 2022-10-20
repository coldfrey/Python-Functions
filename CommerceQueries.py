import requests
import json
from getAuth import authToken


def addOrdersToDict(allOrders, data):

  for order in data['data']:
      orderInfo = {}
      attributes = order['attributes']
      relationships = order['relationships']

      orderID = order['id']
      
      status = attributes["status"]
            
      if status not in allOrders.items():
        allOrders[status] = []
      else:
        allOrders[status].append(orderID)

      
        
      orderInfo['Status'] = status
      orderInfo['OrderDate'] = attributes['payment_updated_at']
      orderInfo['BillingInfo'] = retrieveAddressInfo(relationships, 'billing_address')
      orderInfo['ShippingInfo'] = retrieveAddressInfo(relationships, 'shipping_address')
      orderInfo['CustomerEmail'] = attributes['customer_email']

      orderInfo['UnitDescription'] = None
      orderInfo['UnitQuantity'] = None
      orderInfo['UnitRate'] = None
      orderInfo['TotalPrice'] = attributes['formatted_total_amount_with_taxes']

      allOrders[orderID] = orderInfo

  return allOrders


# Function to make API call to retrieve Billing Info
def retrieveAddressInfo(relationships, arg):
    '''
    Arg is 'shipping_address' or 'billing_address'
    
    '''
    url = relationships[arg]['links']['related']
    
    payload={}
    headers = {
        'Authorization': 'Bearer ' + authToken
    }
    print('Reaching out...')
    response = requests.request("GET", url, headers=headers, data=payload)
    print('Touching me..')
    info = json.loads(response.text)
    print('Touching you..')
    print('request made')
    if info['data'] is not None:
        return info['data']['attributes']['full_address']
    else:
        return 'No ' + arg.replace('_', ' ') + ' provided'
