import RPi.GPIO as GPIO
import time
import camera
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

while True:
    state = GPIO.input(BUTTON)
    if state:
        print("off")
    else:
        print("on")
        os.system("raspistill -h 400 -w 400 -v -o output.jpg")
        camera.uploadToS3('./output.jpg')
        time.sleep(1)
