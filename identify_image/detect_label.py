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
from gtts import gTTS
import os
import logging
import time
import argparse
import json
import pygame



AllowedActions = ['both', 'publish', 'subscribe']


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
parser.add_argument("-t", "--topic", action="store", dest="topic", default="MyThing/label", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = "" #Please enter yourself information
rootCAPath = ""  #Please enter yourself information
certificatePath = "" #Please enter yourself information
privateKeyPath = "" #Please enter yourself information

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
#if args.mode == 'both' or args.mode == 'subscribe':
#    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
#time.sleep(2)


VOICE = 0
result = None
def customCallback(client, userdata, message):
    global VOICE, result
    payload = str(message.payload.decode("utf-8"))
    print('Topic: '+topic+' Payload: '+ payload)
    
    result = json.loads(message.payload)['label']
    print(result)
    VOICE = 1
    #time.sleep(1)
    #os.system('say %s' %result)
    #time.sleep(1)
    #os.system('say %s' %result)



myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

#mqttc.loop_forever()
print('start!')
while True:
    if VOICE == 1:
        VOICE = 0
        tts = gTTS(text=result, lang='en')
        tts.save('hello.mp3')
        print('save as mp3.')
        os.system('mpg321 hello.mp3')
        time.sleep(1)
        os.system('mpg321 hello.mp3')
    #None
#    
#    time.sleep(1)


















