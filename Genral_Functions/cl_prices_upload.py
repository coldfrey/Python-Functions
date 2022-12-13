import json
import os
from dotenv import load_dotenv
from time import sleep


import requests

import importCSV
from uncommonClasses import SKU

# Create the SKUs on Commerce Layer and then make the prices.
# Then link the prices to the SKUs.

# Set the API endpoint
api_endpoint = 'https://uncommon.commercelayer.io/api'

load_dotenv()
# Set the API key

client_secret = os.getenv('COMMERCE_LAYER_CLIENT_SECRET')
client_id = os.getenv('COMMERCE_LAYER_CLIENT_ID')

access_headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
}

access_data = {
  'grant_type': 'client_credentials',
  'client_id': client_id,
  'client_secret': client_secret,
}

response = requests.post('https://uncommon.commercelayer.io/oauth/token?', headers=access_headers, data=json.dumps(access_data))

# Print the response
print(response.json())

# Get the access token
access_token = response.json()['access_token']


print("Starting")
print("Access token: " + access_token)

SHIPPPING_CATEGORY_ID = 'VWoxGFYLrK' # Merchendising

# Set the headers
headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'Bearer %s' % access_token
}




allTaxons = importCSV.importTaxons('TCS1.csv')

  

# get the list of SKUs with associated variant names

def getSKUs(Taxons):
  SKUs = []
  # limit = 0
  for taxon in Taxons:
    for product in taxon.products:
      for variant in product.variants:
        # remove first character of product price
        if product.price == None:
          print("No price for " + product.name['en'])
          # test type of product.price
          print(type(product.price))
          print(product.price)
          continue
        p_price = product.price
        SKUs.append(SKU(variant.sku, p_price, variant.name))
  return SKUs

skuList = getSKUs(allTaxons)

# 
print("Found " + str(len(skuList)) + " unique SKUs")


# Add the SKUs to Commerce Layer

def addSKUs(SKUs):
  for sku in SKUs:
    # Set the query
    data = {
      'data': {
        'type': 'skus',
        'attributes': {
          'code': sku.sku,
          'name': sku.name['en'],
          'do_not_track': True,
          'do_not_ship': False
        },
        'relationships': {
          'shipping_category': {
            'data': {
              'type': 'shipping_categories',
              'id': SHIPPPING_CATEGORY_ID
            }
          }
        }
      }
    }

    # Make the request
    response = requests.post('%s/skus' % api_endpoint, headers=headers, data=json.dumps(data))

    # Print the response
    print(response)


addSKUs(skuList)


def getPricesFromPriceList(id, tag=None):
  response = requests.get('%s/price_lists/%s/prices' % (api_endpoint, id), headers=headers)
  # test we get the first page (10 items)
  priceIDs = []
  for price in response.json()['data']:
    # print(price['attributes']['sku_code'])
    # print(price['id'])
    if tag != None:
      if tag in price['attributes']['sku_code']:
        priceIDs.append((price['attributes']['sku_code'],price['id']))
    else:
      priceIDs.append((price['attributes']['sku_code'],price['id']))
    # print(price['attributes']['amount_cents'])
    # print(price['attributes']['compare_at_amount_cents'])
    # print("")
  # work out how many pages there are from the meta data
  pages = response.json()['meta']['page_count']
  for i in range(2, pages + 1):
    response = requests.get('%s/price_lists/%s/prices?page=%s' % (api_endpoint, id, i), headers=headers)
    for price in response.json()['data']:
      # print(price['attributes']['sku_code'])
      # print(price['id'])
      if tag != None:
        if tag in price['attributes']['sku_code']:
          priceIDs.append((price['attributes']['sku_code'],price['id']))
      else:
        priceIDs.append((price['attributes']['sku_code'],price['id']))
      # print(price['attributes']['amount_cents'])
      # print(price['attributes']['compare_at_amount_cents'])
      # print("")
  return priceIDs

def deletePrice(priceID):
  response = requests.delete('%s/prices/%s' % (api_endpoint, priceID), headers=headers, data=json.dumps({}))
  # Print the response
  print(response)

# for price in getPricesFromPriceList('AlnOyCbYAL', 'TCS'):
#   print('deleting price for ' + price[0])
#   deletePrice(price[1])

    

def getSkusFromSkuList(tag=None):
  response = requests.get('%s/skus' % (api_endpoint), headers=headers)
  # test we get the first page (10 items)
  skuIDs = []
  for sku in response.json()['data']:
    # print(sku['attributes']['code'])
    # print(sku['id'])
    if tag != None:
      if tag in sku['attributes']['code']:
        skuIDs.append((sku['attributes']['code'],sku['id']))
    else:
      skuIDs.append((sku['attributes']['code'],sku['id']))
    # print(sku['attributes']['name'])
    # print("")
  # work out how many pages there are from the meta data
  pages = response.json()['meta']['page_count']
  for i in range(2, pages + 1):
    response = requests.get('%s/skus?page=%s' % (api_endpoint, i), headers=headers)
    for sku in response.json()['data']:
      # print(sku['attributes']['code'])
      # print(sku['id'])
      if tag != None:
        if tag in sku['attributes']['code']:
          skuIDs.append((sku['attributes']['code'],sku['id']))
      else:
        skuIDs.append((sku['attributes']['code'],sku['id']))
      # print(sku['attributes']['name'])
      # print("")
  return skuIDs

def deleteSku(skuID):
  response = requests.delete('%s/skus/%s' % (api_endpoint, skuID), headers=headers, data=json.dumps({}))
  # Print the response
  print(response)

# for sku in getSkusFromSkuList('TCS'):
#   print('deleting SKU ' + sku[0])
#   deleteSku(sku[1])


def addPrices(SKUs):
  # sku = SKUs[0]
    # Set the query
  for sku in SKUs:
    data = {
      'data': {
        'type': 'prices',
        'attributes': {
          'amount_cents': sku.price,
          'compare_at_amount_cents': sku.price,
          'sku_code': sku.sku,
        },
        'relationships': {
          'price_list': {
            'data': {
              'type': 'price_lists',
              'id': 'AlnOyCbYAL'
            }
          }
        }
        
      }
    }

    print("Making price for " + sku.sku)
    # Make the request
    response = requests.post('%s/prices' % api_endpoint, headers=headers, data=json.dumps(data))

    # Print the response
    print("Price response")
    print(response)
  

addPrices(skuList)