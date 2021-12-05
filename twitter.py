'''
Code to get Twitter data via API
'''


import json, tweepy, time, sys, os, random
import tempfile, requests
import urlib.request
from os import environ

'''
api key: bzVIDZamtYW6UKOk1V7DSFThW
api key secret: 7i5cVfdKUobpMVQaz6R1RbM3hhqLuTLSf2qfTRlVd5xcR4uYHk
bearer token: AAAAAAAAAAAAAAAAAAAAANtFWgEAAAAAmNGQiuKLEfM6%2F4KDDy7I8GGyfbw%3DLj3rKK77t0fsr4JvieG0K5ybkyetijAbsB5p8rXRtqJSD7c6ex
'''

#Step 1. Create S3 Bucket, EC2 Instances, Kinesis Stream
session = boto3.Session(profile_name='default')
kinesis = session.client('kinesis')
s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket='lsc-project')

#creating ec2 instance

instances = ec2.create_instances(ImageId='ami-02e136e904f3da870',
                                 MinCount=1,
                                 MaxCount=2,
                                 InstanceType='t2.micro',
                                 KeyName='macs_30123_CB',
                                 SecurityGroupIds=['sg-01f3da276301638af'],
                                 SecurityGroups=['launch-wizard-1'],
                                 IamInstanceProfile=
                                     {'Name': 'EMR_EC2_DefaultRole'},
                                )

# Create Kinesis Stream
try: 
    response = kinesis.create_stream(StreamName='twitter_stream',
                                ShardCount=1
                                )
except Exception:
    pass
waiter = kinesis.get_waiter('stream_exists')
waiter.wait(StreamName='twitter_stream')

# Wait until EC2 instances are running before moving on
waiter = ec2_client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance.id for instance in instances])

code = ['twitter_consumer.py', 'twitter_producer.py']
ssh_producer, ssh_consumer = paramiko.SSHClient(), paramiko.SSHClient()

