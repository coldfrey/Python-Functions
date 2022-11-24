import json
from getAuth import authToken
from lambda_get_all_data.retrieveOrderWindow import retrieveOrderWindow


def lambda_handler(event_data, context):
    # check for order_id and subdomain in keys
    if 'orderWindow' in event_data and 'subdomain' in event_data:
        orderWindow = event_data['orderWindow']
        subdomain = event_data['subdomain']
        allOrders = retrieveOrderWindow(orderWindow=orderWindow, subdomain='uncommon', authToken=authToken)

        # If allOrders is empty, return empty dict
        if not allOrders:
            return {
                'statusCode': 200, 
                'body': json.dumps({'message': 'No orders found'})
            }
        else:
            return {
            'statusCode': 200,
            'body': json.dumps(allOrders)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('No order_id or subdomain provided')
        }



