from http import client
import json

import os

import requests

import importCSV
import uncommonClasses

# Create the SKUs on Commerce Layer and then make the prices.
# Then link the prices to the SKUs.

# Set the API endpoint
api_endpoint = 'https://uncommon.commercelayer.io'

# Set the API key

client_secret = os.getenv('COMMERCE_LAYER_CLIENT_SECRET')
client_id = os.getenv('COMMERCE_LAYER_CLIENT_ID')

SHIPPPING_CATEGORY_ID = 'shipping_category_1'

# Set the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % client_secret
}




allTaxons = importCSV.importTaxons('EPU2.csv')

class SKU:
    def __init__(self, sku, price, name):
        self.sku = sku
        self.price = price
        self.name = name 
    
    def __str__(self):
        return f'{self.sku} {self.price} {self.name}'

  

# get the list of SKUs with associated variant names

def getSKUs(Taxons):
  SKUs = []
  for taxon in Taxons:
    for product in taxon.products:
      for variant in product.variants:
        SKUs.append(SKU(variant.sku, product.price, variant.name))
  return SKUs

skuList = getSKUs(allTaxons)

print(skuList)


# Add the SKUs to Commerce Layer

def addSKUs(SKUs):
  for sku in SKUs:
    # Set the query
    data = {
      'data': {
        'type': 'skus',
        'attributes': {
          'code': sku.sku,
          'name': sku.name
        },
        'relationships': {
          'shipping_category': {
            'data': {
              'type': 'shipping_categories',
              'id': 
      }
    }

    # Print the response
    print(response)

addSKUs(skuList)