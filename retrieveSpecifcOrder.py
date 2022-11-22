import requests
import json
from getAuth import authToken


def formatData(data):
    order = data['data']
    orderInfo = {}
    attributes = order['attributes']
    relationships = order['relationships']

    orderID = order['id']
    status = attributes["status"]
    
    print(orderID, ': ', status)
    
    orderInfo['Status'] = status
    orderInfo['OrderDate'] = attributes['payment_updated_at']
    orderInfo['BillingInfo'] = retrieveAddressInfo(relationships, 'billing_address')
    orderInfo['ShippingInfo'] = retrieveAddressInfo(relationships, 'shipping_address')
    orderInfo['CustomerEmail'] = attributes['customer_email']

    orderInfo['UnitDescription'] = retrieveLineItems(relationships)
    orderInfo['UnitQuantity'] = None
    orderInfo['UnitRate'] = None
    orderInfo['TotalPrice'] = attributes['formatted_total_amount_with_taxes']

    return orderInfo


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

    response = requests.request("GET", url, headers=headers, data=payload)
    
    info = json.loads(response.text)
    
    if info['data'] is not None:
        return info['data']['attributes']['full_address']
    else:
        return 'No ' + arg.replace('_', ' ') + ' provided'


# Function to make API call to line_items
def retrieveLineItems(relationships):
    url = relationships['line_items']['links']['related']
    
    payload={}
    headers = {
        'Authorization': 'Bearer ' + authToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    info = json.loads(response.text)
    line_items_data = info['data']

    line_items = []
    for line_item in line_items_data:
      item_data = extractLineItemData(line_item)
      if item_data is not None:
        line_items.append(item_data)

    return line_items


# Function to extract line_item data
def extractLineItemData(line_item):
    item_data = {}
    
    item_data['id'] = line_item['id']
    attributes = line_item['attributes']

    sku_code = attributes['sku_code']
    if sku_code is None:
      return None

    item_data['sku_code'] = sku_code
    item_data['quantity'] = attributes['quantity']
    item_data['unit_price'] = attributes['formatted_unit_amount']
    item_data['total_price'] = attributes['formatted_total_amount']
    item_data['unit_description'] = attributes['name']
    item_data['image_url'] = attributes['image_url']

    return item_data


def retrieveSpecificOrder(orderID, subdomain, authToken):
    url = "https://" + subdomain + ".commercelayer.io/api/orders/" + orderID

    payload={}
    headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'Bearer ' + authToken
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    # print(data['data']['attributes'])
    order = formatData(data)
    return order