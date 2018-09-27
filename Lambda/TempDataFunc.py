from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # TODO implement

    print(event)
    temperature = str(event['temperature'])
    humidity = str(event['humidity'] )
    time_now = str(event['time'])
    seat_time = str(event['seat_time'])
    sound_count = str(event['sound'])
    isCrying = str(event['isCrying'])
    
    print("humidity", humidity)
    
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('TempData') #Table name


    table.update_item(
        Key={'Key_': 'humidity'},
        UpdateExpression="SET TimeStamp_=:a, Value_=:p",
        ExpressionAttributeValues={
            ':a': time_now,
            ':p': humidity
        }
    )

    table.update_item(
        Key={'Key_': 'temperature'},
        UpdateExpression="SET TimeStamp_=:a, Value_=:p",
        ExpressionAttributeValues={
            ':a': time_now,
            ':p': temperature
        }
    )
    
    table.update_item(
        Key={'Key_': 'lastSeat'},
        UpdateExpression="SET TimeStamp_=:a, Value_=:p",
        ExpressionAttributeValues={
            ':a': seat_time,
            ':p': None
        }
    )
    
    table.update_item(
        Key={'Key_': 'sound'},
        UpdateExpression="SET TimeStamp_=:a, Value_=:p",
        ExpressionAttributeValues={
            ':a': sound_count,
            ':p': isCrying
        }
    )
    
    
    if isCrying == "1":
        sns = boto3.resource('sns', region_name='us-east-1')
        topic = sns.Topic('') #Please enter your Topic
        response = topic.publish(Message='Your baby is CRYING.QQ')
   