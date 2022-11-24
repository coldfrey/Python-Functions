import json
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import order_summary_pdf_gen as pdf
from getAuth import authToken

# UNCOMMENT THE BELOW CODE TO GENERATE PDF 
# create_pdf("CA-report.pdf")


def lambda_handler(event_data, context):
    event_body = json.loads(event_data['body'])
    order_id = event_body['order_id']
    subdomain = "uncommon"
    print(type(event_data))

    #for testing on lambda dont load the json- already loaded
    # event_body = event_data['body']
    # order_id = event_body['order_id']
        
    pdf.create_pdf(order_id, subdomain, authToken)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "The Boyz <maxm@uncommongroup.com>"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "jack@captainapp.co.uk"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-2"

    # The subject line for the email.
    SUBJECT = "Captain App Report"

    # The full path to the file that will be attached to the email.
    ATTACHMENT = "/tmp/OrderSummary_" + order_id + ".pdf"
    # create_pdf("CA-report.pdf")
    BODY_TEXT = "Hello,\r\nPlease see the attached file for a list of customers to contact."

    #import html file
    # with open('email.html', 'r') as myfile:
    #     data=myfile.read()
    #     BODY_HTML = data
    BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>Hello!</h1>
        <p>Please see the attached file for the report breakdown.</p>
        </body>
        </html>
        """
    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)
    # print(msg)
    # return{
    #     'statusCode': 200,
    #     'body': json.dumps('email loaded')
    # }
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT,
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            # ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('Confirmation Email Sent!')
    }
