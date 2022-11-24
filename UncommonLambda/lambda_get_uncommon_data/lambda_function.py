import json
from getAuth import authToken
from retrieveSpecificOrder import retrieveSpecificOrder


def lambda_handler(event_data, context):
    # check for order_id and subdomain in keys
    if 'order_id' in event_data and 'subdomain' in event_data:
        order_id = event_data['order_id']
        subdomain = event_data['subdomain']
        order = retrieveSpecificOrder(order_id, subdomain, authToken)
        return {
            'statusCode': 200,
            'body': json.dumps(order)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('No order_id or subdomain provided')
        }

