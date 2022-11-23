import requests
import json
from getAuth import authToken
from datetime import datetime, timedelta


def formatData(allOrders, data, maxDate):
    """
    Formats data from API call into a dictionary
    
    Args:
        data (dict): Data from API call
        allOrders (dict): Dictionary to add data to
        maxDate (str): Date to stop adding orders to dictionary

    Returns:
        allOrders (dict): Dictionary of all orders
        exitCode (int): -1 if max date reached, 1 if another paeg of orders to retrieve  
        """
    orderList = data['data']

    # Reverse order list so that most recent orders are first
    orderList.reverse()

    for order in orderList:
      orderInfo = {}
      attributes = order['attributes']
      relationships = order['relationships']

      orderID = order['id']
      status = attributes["status"]
      
      print(orderID, ': ', status)
      if status != 'placed':
        continue

        
      orderInfo['Status'] = status
      date = attributes['payment_updated_at']

      # Check if order is within orderWindow
      if date < maxDate:
        exitCode = -1
        return allOrders, exitCode
      
      orderInfo['OrderDate'] = date
      orderInfo['BillingInfo'] = retrieveAddressInfo(relationships, 'billing_address')
      orderInfo['ShippingInfo'] = retrieveAddressInfo(relationships, 'shipping_address')
      orderInfo['CustomerEmail'] = attributes['customer_email']

      orderInfo['UnitDescription'] = retrieveLineItems(relationships)
      orderInfo['UnitQuantity'] = None
      orderInfo['UnitRate'] = None
      orderInfo['TotalPrice'] = attributes['formatted_total_amount_with_taxes']

      allOrders[orderID] = orderInfo
    
    exitCode = 1
    return allOrders, exitCode
    

def retrieveAddressInfo(relationships, arg):
    '''
    Function to make API call to retrieve billing or shipping info

    Args:
        relationships (dict): Relationships dictionary from order data
        arg (str): 'billing_address' or 'shipping_address'

    Returns:
        addressInfo (dict): Dictionary of address info
    
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


def retrieveLineItems(relationships):
    """
    Function to make API call to retrieve line items

    Args:
        relationships (dict): Relationships dictionary from order data

    Returns:
        unitDescription (str): String of all line items

    """
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
    """
    Function to extract line item data

    Args:
        line_item (dict): Dictionary of line item data

    Returns:
        item_data (str): String of line item data
    """
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


def retrieveOrderWindow(orderWindow, subdomain, authToken):
    """
    Retrieves all placed orders between time of api call and specified window duration

    Args:
        orderWindow (int): Number of days to look back for orders
        subdomain (str): Subdomain of Commerce Layer account
        authToken (str): Auth token for Commerce Layer account
    
    """
    # Get current date and time
    now = datetime.now()
    # Get date and time of orderWindow days ago
    maxDate = now - timedelta(days=orderWindow)
    # Convert to ISO 8601 format
    maxDate = maxDate.isoformat()

    # Set up API call
    url = "https://" + subdomain + ".commercelayer.io/api/orders"

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

    # Loop through all pages of orders
    while 1:
        urlDict = data['links']

        if pageNumber == 0:
            url = data['links']['last']
            response = requests.request("GET", url, headers=headers, data=payload)
            data = json.loads(response.text)
            allOrders, exitCode = formatData(allOrders, data, maxDate)
            
            if exitCode == -1:
                break
            else:
                pageNumber += 1
                continue

        elif 'prev' in urlDict.keys():
            # Request next page
            url = data['links']['prev']
            response = requests.request("GET", url, headers=headers, data=payload)
            data = json.loads(response.text)
            allOrders, exitCode = formatData(allOrders, data, maxDate)
            
            if exitCode == -1:
                break
            else:
                pageNumber += 1
        
        else:
            break

    return allOrders


if __name__ == "__main__":

    allOrders = retrieveOrderWindow(orderWindow=90, subdomain='uncommon', authToken=authToken)
    print(allOrders)


