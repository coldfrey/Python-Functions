# Connect to the Sanity API to clear all the data for testing.

import requests
import json

# Set the API key
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

# Set the query to get the ids of every document in the dataset
query = {
    'query': '*[_type == "product" || _type == "catalog" || _type == "country" || _type == "variant" || _type == "taxon" || _type == "taxonomy" || _type == "customer"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

# Get the ids of the documents
ids = [doc['_id'] for doc in response.json()['result']]

# Set the mutation to delete all the documents
mutation = {
  'mutations': [
    {
      'delete': {
        'id': id
      }
    } for id in ids
  ]
}

# Make the request
response = requests.post(api_endpoint_mutate, data=json.dumps(mutation), headers=headers)

print(response.json())

