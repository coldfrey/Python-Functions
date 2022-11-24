# Connect to the Sanity API to Add the data that does not come from the CSV.

import json

import requests

# Set the API key
api_key = 'skdvPrsX0H14MCyNQhgb1Gkz92AVOAnfsKubLgRyG88JUtNINPJIoxj23ijMI1ffQZgckXnzSNztTzVX80zgq7G7J3rQaPKbo0a4XQl2XmWUB9wLc7lLjW7plojlBRG9S7k41SdlrONACACavE418Wf8yDBi54KdzYh35WeA2tCDhRFKzR58'

# datasets: production | uncommon (uncommon is a test dataset)
dataset = 'uncommon' # whilst we test the code let's use the uncommon dataset


# Set the API endpoints
api_endpoint_mutate = 'https://9zkzbvc9.api.sanity.io/v1/data/mutate/%s' % dataset
api_endpoint_query = 'https://9zkzbvc9.api.sanity.io/v1/data/query/%s' % dataset



# Set the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % api_key
}


def randomKey():
    import random
    import string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def seededKey(seed):
    import random
    import string
    random.seed(seed)
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

# The clearDataset.py code will be ran before this code is ran.

# First add the countries
# Set the mutation to add the countries
# country format:
#   "_type": "country",
#   "name": localeString,
#   "code": string,
#   "marketId": string,
#   "defaultLocale": string,

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'country',
        'name': {
          'en': 'United Kingdom of Great Britain and Northern Ireland'
        },
        'code': 'GB',
        'marketId': '11034',
        'defaultLocale': 'en',
        '_id': 'country-' + seededKey('United Kingdom of Great Britain and Northern Ireland'),
      }
    },
    {
      'createOrReplace': {
        '_type': 'country',
        'name': {
          'en': 'Germany'
        },
        'code': 'DE',
        'marketId': '1228',
        'defaultLocale': 'en',
        '_id': 'country-' + seededKey('Germany'),
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

print(response.json())

# Add the Taxons
# Set the mutation to add the taxons
# taxon format:
#   "_type": "taxon",
#   "name": localeString,
#   "label": localeString,
#   "slug": localeSlug,
#   "description": localeString,

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'taxon', 
        'name': {
          'en': 'Envision Accessories'
        },
        'label': {
          'en': 'Accessories'
        },
        'slug': {
          'en': {
            '_type': 'slug',
            'current': 'envision-accessories'
          }
        },
        'description': {
          'en': 'Envision Accessories'
        },
        '_id': 'taxon-' + seededKey('Envision Accessories'),
      }
    },
    {
      'createOrReplace': {
        '_type': 'taxon',
        'name': {
          'en': 'Envision Clothing'
        },
        'label': {
          'en': 'Clothing'
        },
        'slug': {
          'en': {
            '_type': 'slug',
            'current': 'envision-clothing'
          }
        },
        'description': {
          'en': 'Envision Clothing'
        },
        '_id': 'taxon-' + seededKey('Envision Clothing'),
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

# Get reference to the taxons (query for the taxons)
query = {
  'query': '*[_type == "taxon"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

# Get the ids of the taxons
ids = [doc['_id'] for doc in response.json()['result']]


# Add the taxonomy
# Set the mutation to add the taxonomy
# taxonomy format:
#   "_type": "taxonomy",
#   "name": localeString,
#   "label": localeString,
#   "taxons": array of taxon references,

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'taxonomy',
        'name': {
          'en': 'Envision Categories'
        },
        'label': 'Category',
        'taxons': [
          {
            '_key': randomKey(),
            '_type': 'reference',
            '_ref': ids[0]
          },
          {
            '_key': randomKey(),
            '_type': 'reference',
            '_ref': ids[1]
          }
        ],
        '_id': 'taxonomy-' + seededKey('Envision Categories'),
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

# Get reference to the taxonomy (query for the taxonomy)
query = {
  'query': '*[_type == "taxonomy"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

# Get the id of the taxonomy
id = response.json()['result'][0]['_id']

# Add the Catalogue

# Set the mutation to add the catalogue
# catalogue format:
#   "_type": "catalog",
#   "name": localeString,
#   "taxonomies": array of taxonomy references,

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'catalog',
        'name': {
          'en': 'Envision Catalogue'
        },
        'taxonomies': [
          {
            '_key': randomKey(),
            '_type': 'reference',
            '_ref': id
          }
        ],
        '_id': 'catalog-' + seededKey('Envision Catalogue'),
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

# Get reference to the catalogue (query for the catalogue)
query = {
  'query': '*[_type == "catalog"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

# Get the id of the catalogue
id = response.json()['result'][0]['_id']

# Add the customer
# Set the mutation to add the customer
# customer format:
#   "_type": "customer",
#   "name": string
#   "slug": slug,
#   "code": string,
#   "catalog": reference to catalogue,
#   "defaultLocale": string,

mutation = {
  'mutations': [
    {
      'createOrReplace': {
        '_type': 'customer',
        'name': 'Envision',
        'slug': {
          '_type': 'slug',
          'current': 'envision'
        },
        'code': 'envision',
        'catalog': {
          '_key': randomKey(),
          '_type': 'reference',
          '_ref': id
        },
        'defaultLocale': 'en',
        '_id': 'customer-' + seededKey('Envision'),
      }
    }
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

print(response.json())

def addColor():
  from uncommonClasses import Color
  color = Color("N/A")

  # Set the mutation to add the color
  # color format:
  #   "_type": "color",
  #   "name": string
  mutations = []
  mutations.append({
    'createOrReplace': {
      '_type': 'color',
      'name': color.name,
      '_id': 'color-' + seededKey(color.name['en']),
    }
  })

  mutation = {
    'mutations': mutations
  }

  # Make the request
  response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

  
addColor()