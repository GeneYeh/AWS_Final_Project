'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

import sys
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
#parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
#parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
#parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
#parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
#parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
#                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/data", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = "" #Please enter yourself information
rootCAPath = "" #Please enter yourself information
certificatePath = "" #Please enter yourself information
privateKeyPath = "" #Please enter yourself information
#useWebsocket = args.useWebsocket
clientId = "" #Please enter your clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

#if args.useWebsocket and args.certificatePath and args.privateKeyPath:
#    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
#    exit(2)

#if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
#    parser.error("Missing credentials for authentication.")
#    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
#if useWebsocket:
#    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
#    myAWSIoTMQTTClient.configureEndpoint(host, 443)
#    myAWSIoTMQTTClient.configureCredentials(rootCAPath)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

#sensor parameter
DHT11 = Adafruit_DHT.DHT11
DHT_pin = 4
humidity, temperature = Adafruit_DHT.read_retry(DHT11, DHT_pin)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

PIR = 7

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.setup(PIR, GPIO.IN)
print "Waiting for sensor to settle"
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
last_time = time.time()
WAITING_TIME = 10
while True:
    cur_time = time.time();
    period = cur_time - last_time;
    
    if period >= WAITING_TIME:
        humidity, temperature = Adafruit_DHT.read_retry(DHT11, DHT_pin)
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(0.1)
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            pass
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            pass
        stop = time.time()
        elapsed = stop - start
        distance = elapsed * 34000 / 2

        if args.mode == 'both' or args.mode == 'publish':
            message = {}
            message['temperature'] = temperature
            message['humidity'] = humidity
            message['time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            message['distance'] = distance
            message['sequence'] = loopCount
            message['Motion'] = GPIO.input(PIR)
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            
            if humidity is not None and temperature is not None:
                print('Temp={0:0.5f}*  Humidity={1:0.5f}%'.format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')

            if args.mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))
            loopCount += 1
        last_time = time.time()


















