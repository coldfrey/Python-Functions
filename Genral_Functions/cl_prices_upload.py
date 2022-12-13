import json
import os
from dotenv import load_dotenv


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

response = requests.post('https://uncommon.commercelayer.io/oauth/token?',
                         headers=access_headers, data=json.dumps(access_data))

# Print the response
print(response.json())

# Get the access token
access_token = response.json()['access_token']


print("Starting")
print("Access token: " + access_token)

SHIPPPING_CATEGORY_ID = 'VWoxGFYLrK'  # Merchendising

# Set the headers
headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'Bearer %s' % access_token
}


allTaxons = importCSV.importTaxons('EPU2.csv')


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
                p_price = int(float(product.price[1:])*100)
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
        response = requests.post(
            '%s/skus' % api_endpoint, headers=headers, data=json.dumps(data))

        # Print the response
        print(response)

# addSKUs(skuList)


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
        response = requests.post(
            '%s/prices' % api_endpoint, headers=headers, data=json.dumps(data))

        # Print the response
        print("Price response")
        print(response)


addPrices(skuList)
