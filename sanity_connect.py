# Connect to the Sanity API

import requests
import json

# Notes for Andre:

# There is a limit of 100,000 API calls per month. We are currently at 75. So we're probably good.
# Below is live example of querying Sanity and uploading to Sanity.

# I'm not sure that the 'createOrUpdate' is working. Please figure this out.
# We also need to create varients and query to list their ids.
# then add these ids to the product object.

# Set the API key
# Note that this API key will work for now. I will invalidate it on Monday.
api_key = 'skdvPrsX0H14MCyNQhgb1Gkz92AVOAnfsKubLgRyG88JUtNINPJIoxj23ijMI1ffQZgckXnzSNztTzVX80zgq7G7J3rQaPKbo0a4XQl2XmWUB9wLc7lLjW7plojlBRG9S7k41SdlrONACACavE418Wf8yDBi54KdzYh35WeA2tCDhRFKzR58'

# datasets: production | uncommon (uncommon is a test dataset)
dataset = 'uncommon' # whilst we test the code let's use the uncommon dataset

# Set the API endpoints
api_endpoint_query = 'https://9zkzbvc9.api.sanity.io/v1/data/query/%s' % dataset
api_endpoint_mutate = 'https://9zkzbvc9.api.sanity.io/v1/data/mutate/%s' % dataset



# Set the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % api_key
}

# Set the query
query = {
    'query': '*[_type == "product"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

print(response.json())

# Demo mutation - update or insert a product with the following properties: 
# name - localeString - "Test Product"
# description - localeText - "This is a test product"
# composition - localeText - "100% Cotton"
# coo - string - "China"
# slug - localeSlug - "test-product"
# minimumOrderQuanity - number - 100
# orderIncrement - number - 100
# reference - string - "123456789"
# leadtime - string - "10 weeks"

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'product',
        'name': {
          'en': 'Test Product'
        },
        'description': {
          'en': 'This is a test product'
        },
        'composition': {
          'en': '100% Cotton'
        },
        'coo': 'China',
        'slug': {
          'en': {
            '_type': 'slug',
            'current': 'test-product'
          }
        },
        'minimumOrderQuantity': 100,
        'orderIncrement': 100,
        'reference': '123456789',
        'leadtime': '10 weeks'
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

print(response.json())