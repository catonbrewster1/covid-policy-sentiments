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

BUCKET_NAME = 'lsc-tweets'
kinesis = boto3.client('kinesis', region_name='us-east-1')
s3 = boto3.client('s3')

# Simulate streaming Twitter data
# Loop through tweets from s3 bucket and feed into kinesis
s3_rec = boto3.resource('s3')
my_bucket = s3_rec.Bucket(BUCKET_NAME)
for files in my_bucket.objects.all():
    file_name = files.key
    print(file_name)
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
    obj_ser = obj["Body"].read()
    data = pickle.loads(obj_ser)
    for i in data.keys():
            tweet = {}
            tweet["id"] = data[i]["id"]
            tweet["tweet"] = data[i]["tweet"]
            tweet["geo"] = data[i]["geo"]
            tweet["date"] = data[i]["date"]
            kinesis.put_record(StreamName="twitter_stream",
                            Data=json.dumps(tweet),
                            PartitionKey="partitionkey")

    