import json
from getAuth import authToken
from retrieveSpecificOrder import retrieveSpecificOrder

def lambda_handler(event, context):
    order_id = event['order_id']
    subdomain = event['subdomain']
    order = retrieveSpecificOrder(order_id, subdomain, authToken)
    return order

