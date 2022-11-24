import requests
import json

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

# get the ids of all the taxons
query = {
    'query': '*[_type == "taxon"]'
}

# Make the request
response = requests.post(api_endpoint_query, data=json.dumps(query), headers=headers)

# Get the ids of the documents
ids = [doc['_id'] for doc in response.json()['result']]
print(ids)