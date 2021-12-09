import boto3
import time
import random
import datetime
import json
import twint
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import pickle

kinesis = boto3.client('kinesis', region_name='us-east-1')
s3 = boto3.client('s3')

# Get data from S3 Bucket
obj = s3.get_object(Bucket='lsc-tweets', Key='tweets.json')
obj_ser = obj["Body"].read()
data = pickle.loads(obj_ser)

while True:
    # Simulate streaming data by continuously looping through tweets
    for i in data.keys():
        kinesis.put_record(StreamName="twitter_stream",
                       Data=json.dumps(data[i]),
                       PartitionKey="partitionkey")

    