import json
from getAuth import authToken
from retrieveSpecificOrder import retrieveSpecificOrder


def lambda_handler(event_data, context):
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(event_data['body'])
    # }

    # dejsonify the event data['body']
    event_body = json.loads(event_data['body'])
    # typical event_body: '{"order_id": "1234567890", "subdomain": "myshop"} as string
    # convert to dict
    # event_body = json.loads(event_body)
    order_id = event_body['order_id']
    subdomain = "uncommon"
    order = retrieveSpecificOrder(order_id, subdomain, authToken)
    return{
        'statusCode': 200,
        'body': json.dumps(order)
    }

    # subdomain = "uncommon"
    # if "order_id" not in event_body:
    #     return {
    #         'statusCode': 404,
    #         'body': json.dumps('No order ID provided')
    #     }
    # order_id = event_body["order_id"]
    # order = retrieveSpecificOrder(order_id, subdomain, authToken)
    
    # return {
    #     'statusCode': 200,
    #     'body': order
    # } 
    
        


    # order_id = event_data['order_id']
    # if(order_id is None):
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps('No order ID provided')
    #     }
    # else:
    #     order = retrieveSpecificOrder(order_id, "uncommon", authToken)
    #     return {
    #         'statusCode': 200,
    #         'body': json.dumps(order)
    #     }


    # if (event_data['body']):
    #     body = event_data['body']
    #     if (body.order_id):
    #         order_id = body.order_id;
    #         # subdomain = event_data['subdomain']
    #         order = retrieveSpecificOrder(order_id, "uncommon", authToken)
    #         return {
    #             'statusCode': 200,
    #             'body': json.dumps(order)
    #         }
    #     else:
    #         return {
    #             'statusCode': 400,
    #             'body': json.dumps('No order_id or subdomain provided')
    #         }

