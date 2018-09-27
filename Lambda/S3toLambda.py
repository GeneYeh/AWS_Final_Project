import boto3
import json


BUCKET = "" #Please enter your bucketname
KEY = "output.jpg" #Please enter your image that you want to identify
animal_list = ["Lion", "Hand", "Dog", "Frog", "Cow", "Horse", "Duck", "Dolphin"] #identified list
def detect_labels(bucket, key,max_labels=10, min_confidence=10):
	rekognition = boto3.client("rekognition", 'us-east-1')

	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']

def lambda_handler(event, context):
    for row in detect_labels(BUCKET, KEY):
        print(row)
        if(row["Name"] in animal_list):
            animal_label = row["Name"]
            break
        else:
            animal_label = "Please take a picture again."
    print(animal_label)
            
    iot = boto3.client('iot-data', region_name='us-east-1')

    # Change topic, qos and payload
    response = iot.publish(
        topic='MyThing/label',
        qos=1,
        payload=json.dumps({"label":animal_label})
    )
    