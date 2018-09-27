import boto3
import pygame
import time
import os

def uploadToS3(filePath):
    access_key = '' #Please enter your access_key
    secret_key = '' #Please enter your secret_key

    s3 = boto3.client(
            's3',
            region_name = 'us-east-1',
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key
    )
    bucketname = '' #Please enter your S3 bucketname 
    s3.upload_file(filePath,bucketname,'output.jpg')
    
    print("Upload successful")

uploadToS3('./output.jpg')
