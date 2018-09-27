from __future__ import print_function
import boto3
import json

region_name = 'us-east-1'
# Get the service resource
sns = boto3.resource('sns', region_name)
topic = sns.Topic('') #Please enter your Topic

def lambda_handler(event, context):
    print(event)
    
    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])       
    print('Successfully processed %s records.' % str(len(event['Records'])))
    
    try:
        response = topic.publish(
            Message=str
        )
    except:
        print('The queue is empty.');

