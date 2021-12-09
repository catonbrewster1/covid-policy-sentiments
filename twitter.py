'''
Code to get Twitter data via API
'''


import boto3
import time
import random
import datetime
import json
import paramiko
import tweepy
from scp import SCPClient

'''
api key: bzVIDZamtYW6UKOk1V7DSFThW
api key secret: 7i5cVfdKUobpMVQaz6R1RbM3hhqLuTLSf2qfTRlVd5xcR4uYHk
bearer token: AAAAAAAAAAAAAAAAAAAAANtFWgEAAAAAmNGQiuKLEfM6%2F4KDDy7I8GGyfbw%3DLj3rKK77t0fsr4JvieG0K5ybkyetijAbsB5p8rXRtqJSD7c6ex
'''

#Step 1. Create S3 Bucket, EC2 Instances, Kinesis Stream
session = boto3.Session(profile_name='default')
kinesis = session.client('kinesis')
s3 = boto3.client('s3')

ec2 = session.resource('ec2')
ec2_client = session.client('ec2')

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

# Wait until EC2 instances are running before moving on
waiter = ec2_client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance.id for instance in instances])

# Get producer/consumer code running on EC2 instances
instance_dns = [instance.public_dns_name 
                 for instance in ec2.instances.all() 
                 if instance.state['Name'] == 'running'
               ]
code = ['twitter_consumer.py', 'twitter_producer.py']
ssh_producer, ssh_consumer = paramiko.SSHClient(), paramiko.SSHClient()
print(ssh_producer, ssh_consumer)

# Install boto3 on each EC2 instance and Copy our producer/consumer code onto producer/consumer EC2 instances
instance = 0
stdin, stdout, stderr = [[None, None] for i in range(3)]
for ssh in [ssh_producer, ssh_consumer]:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(instance_dns[instance],
                username = 'ec2-user',
                key_filename='/Users/catonbrewster/Box Sync/Y2 - Q1 Fall/LSC/Project/covid-policy-sentiments/macs_30123_CB.pem')
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(code[instance])
    
    if instance == 0:
        stdin[instance], stdout[instance], stderr[instance] = \
            ssh.exec_command("sudo pip3 install boto3")
    else:
        stdin[instance], stdout[instance], stderr[instance] = \
            ssh.exec_command("sudo pip3 install boto3")

    instance += 1

# Block until Producer has installed boto3 and testdata, then start running Producer script:
producer_exit_status = stdout[0].channel.recv_exit_status() 
if producer_exit_status == 0:
    ssh_producer.exec_command("python3 %s" % code[0])
    print(code[0])
    print("Producer Instance is Running twitter_producer.py\n.........................................")
else:
    print("Error", producer_exit_status)

# Block until Consumer has installed boto3 and testdata, then start running Consumer script:
consumer_exit_status = stdout[1].channel.recv_exit_status() 
if consumer_exit_status == 0:
    ssh_producer.exec_command("python3 %s" % code[1])
    print(code[1])
    print("Consumer Instance is Running twitter_consumer.py\n.........................................")
else:
    print("Error", consumer_exit_status)

# Close ssh
ssh_consumer.close; ssh_producer.close()


# check bucket
my_bucket = bucket
for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object.key)


'''# (for personal use): Delete everything as needed
s3 = boto3.resource('s3')
bucket = s3.Bucket('lsc-project-2')
bucket.objects.all().delete()
bucket.delete()

ec2 = boto3.resource('ec2')
ids = []
for instance in ec2.instances.all():
    ids.append(instance.id)
ec2.instances.filter(InstanceIds = ids).terminate()

response = client.delete_stream(
    StreamName='twitter_stream',
    EnforceConsumerDeletion=True)
waiter = kinesis.get_waiter('stream_deleted')
waiter.wait(StreamName='twitter_stream')

'''