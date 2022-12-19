import json
import os

import requests
from dotenv import load_dotenv

import importCSV
import uncommonClasses

# Connect to the Sanity API
# Notes for Andre:

# There is a limit of 100,000 API calls per month. We are currently at 75. So we're probably good.
# Below is live example of querying Sanity and uploading to Sanity.

# I'm not sure that the 'createOrUpdate' is working. Please figure this out.
# We also need to create varients and query to list their ids.
# then add these ids to the product object.

# Set the API key
load_dotenv()
api_key = os.getenv('SANITY_API_KEY')
# datasets: production | uncommon (uncommon is a test dataset)
dataset = 'test' # whilst we test the code let's use the uncommon dataset

# Set the API endpoints
api_endpoint_query = 'https://9zkzbvc9.api.sanity.io/v1/data/query/%s' % dataset
api_endpoint_mutate = 'https://9zkzbvc9.api.sanity.io/v1/data/mutate/%s' % dataset



# Set the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % api_key
}

# Set the query
# query = {
#     'query': '*[_type == "product"]'
# }



# mutation = {
#   'mutations': [
#     {
#       'createOrReplace': {
#         '_type': 'product',
#         'name': {
#           'en': 'Test Product'
#         },
#         'description': {
#           'en': 'This is a test product'
#         },
#         'composition': {
#           'en': '100% Cotton'
#         },
#         'coo': 'China',
#         'slug': {
#           'en': {
#             '_type': 'slug',
#             'current': 'test-product'
#           }
#         },
#         'minimumOrderQuantity': 100,
#         'orderIncrement': 100,
#         'reference': '123456789',
#         'leadtime': '10 weeks'
#       }
#     }
#   ]
# }


# AllTaxons = importCSV.importTaxons('EPU2.csv')
AllTaxons = importCSV.importTaxons('TCS1.csv')

#print all taxons
# print(AllTaxons)

# get a list of unique sizes from variants within products within taxons
def getUniqueSizes(Taxons):
  sizes = []
  for taxon in Taxons:
    for product in taxon.products:
      for variant in product.variants:
        if variant.size not in sizes:
          sizes.append(variant.size)
  return sizes

sizes = getUniqueSizes(AllTaxons)
# print(sizes)


def populateVariants(Product):
  variants = []
  for variant in Product.variants:
    variants.append({
      'name': variant.name,
      'sku': variant.sku,
      'barcode': variant.barcode,
      'size': variant.size,
      # 'colour': variant.colour,
      })

  return variants


def populateProducts(Taxon):
  products = []
  for product in Taxon.products:
    products.append({
      'name': product.name,
      # 'description': product.description,
      'composition': product.composition,
      'coo': product.coo,
      'slug': product.slug,
      'minimumOrderQuantity': product.moq,
      'orderIncrement': product.oqi,
      'reference': product.reference,
      # 'leadtime': product.leadtime,
      'variants': populateVariants(product)
      })

  return {products}

def getNAColorRef():
  query = {
      'query': '*[_type == "color" && name.en == "N/A"]'
  }

  # query Sanity for sizes
  response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

  # convert the response to JSON
  response = response.json()
  # print(json.dumps(response, indent=2, sort_keys=True))

  # find the NA color
  for result in response['result']:
    if result['name']['en'] == 'N/A':
      print("NA Color found: " + result['_id'])
      return result['_id']

  # convert each result to a size object
  sanityColor = uncommonClasses.Color(response['result'][0]['name']['en'], reference=response['result'][0]['_id'])

  return sanityColor.reference

colorRef = getNAColorRef()

def checkSanitySizes(sizes):
  query = {
      'query': '*[_type == "size"]'
  }

  # query Sanity for sizes
  response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

  # convert the response to JSON
  response = response.json()
  # print(json.dumps(response, indent=2, sort_keys=True))

  # convert each result to a size object
  sanitySizes = []
  for result in response['result']:
    sanitySizes.append(uncommonClasses.Size(result['name']['en'], size_type=result['gender'], reference=result['_id']))
    
  # print("Local Sizes:")
  # print(sizes[-3])
  # print("Sanity Sizes:")
  # print(sanitySizes[1])

  # if sanitySizes[1] == sizes[-3]:
  #   print("Sizes match")
  # OUTPUT: Sizes match
  
  # Finds other matches between the two lists
  for size in sizes:
    for sanitySize in sanitySizes:
      if size == sanitySize:
        # print("Match found")
        # print(size)
        # print(sanitySize)
        # update local size with sanity size reference
        size.reference = sanitySize.reference
        # print(size)
  
  # if any sizes don't have a reference, create one
  for size in sizes:
    if size.reference == "":
      size.generateReference()
  
checkSanitySizes(sizes)

# update all the taxons with the new sizes
for taxon in AllTaxons:
  for product in taxon.products:
    for variant in product.variants:
      for size in sizes:
        if variant.size == size:
          variant.size = size

# print(AllTaxons[0].products[0].variants[0].size)

# create or replace sizes in Sanity
def createOrUpdateSizes(sizes):
  mutations = []
  for size in sizes:
    mutations.append({
      'createOrReplace': {
        '_type': 'size',
        '_id': size.reference,
        'name': {
          'en': size.name
        },
        'gender': size.size_type
      }
    })
    
  mutation = {
    'mutations': mutations
  }

  # print(json.dumps(mutation, indent=2, sort_keys=True))

  # create or update sizes
  response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

  # convert the response to JSON
  response = response.json()
  print(json.dumps(response, indent=2, sort_keys=True))

createOrUpdateSizes(sizes)

# create or replace all variants
def createOrUpdateVariants(Taxons):
  mutations = []
  for taxon in Taxons:
    for product in taxon.products:
      for variant in product.variants:
        mutations.append({
          'createOrReplace': {
            '_type': 'variant',
            '_id': variant.id,
            'name': variant.name,
            'code': variant.sku,
            'barcode': str(variant.barcode),
            'size': {
              '_type': 'reference',
              '_ref': variant.size.reference
            },
            'color': {
              '_type': 'reference',
              '_ref': colorRef # lol note this is GLOBAL
            }
            
          }
        })
  
  mutation = {
    'mutations': mutations
  }

  # print(json.dumps(mutation, indent=2, sort_keys=True))
  print("Number of variants CoR: " + str(len(mutations)))
  # create or update variants
  response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

  # convert the response to JSON
  response = response.json()
  print(json.dumps(response, indent=2, sort_keys=True))

createOrUpdateVariants(AllTaxons)

# create or replace all products
def createOrUpdateProducts(Taxons):
  mutations = []
  for taxon in Taxons:
    for product in taxon.products:
      mutations.append({
        'createOrReplace': {
          '_type': 'product',
          '_id': product.id,
          'name': product.name,
          'label': product.label,
          # 'description': product.description,
          'composition': product.composition,
          'coo': product.coo,
          'slug': product.slug,
          'minimumOrderQuantity': product.moq,
          'orderIncrement': product.oqi,
          'reference': product.reference,
          'variants': [
            {
              '_type': 'reference',
              '_ref': variant.id,
              '_key': variant.key
            } for variant in product.variants
          ]
        }
      })
  
  mutation = {
    'mutations': mutations
  }

  print(json.dumps(mutation, indent=2, sort_keys=True))
  print("Number of products CoR: " + str(len(mutations)))
  # create or update products
  response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

  # convert the response to JSON
  response = response.json()
  print(json.dumps(response, indent=2, sort_keys=True))

createOrUpdateProducts(AllTaxons)

# Add variants to products
def addVariantsToProducts(Taxons):
  mutations = []
  for taxon in Taxons:
    for product in taxon.products:
      mutations.append({
        "patch": {
          # '_type': 'product',
          "id": product.id,
          "insert": {
            "after": "variants",
            "items": [
              {
                "_type": "reference",
                "_ref": variant.id,
                "_key": variant.key
              }
              for variant in product.variants
            ]
          }
        }
      })

  
  mutation = {
    "mutations": mutations
  }

  # print(json.dumps(mutation, indent=2, sort_keys=True))
  print("Number of products with variants to patch: " + str(len(mutations)))
  # create or update products
  response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

  # convert the response to JSON
  response = response.json()
  print(json.dumps(response, indent=2, sort_keys=True))

addVariantsToProducts(AllTaxons)