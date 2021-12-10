import boto3
import io
import os
import json
import twint
import nest_asyncio
nest_asyncio.apply()
from datetime import date, timedelta
import time
import pickle

bucket_name = 'lsc-tweets-mini'
s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket=bucket_name)


c = twint.Config()
c.Search = "covid"
c.Pandas = True
c.Limit = 1000
twint.run.Search(c) 
df = twint.storage.panda.Tweets_df
df_dict = df.to_dict('index')
serialized_dict = pickle.dumps(df_dict)
if df_dict: 
    file_name = "tweets.json"

    response = s3.put_object(Bucket=bucket_name, Key=file_name, Body=serialized_dict)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")
else: 
    print("not added")



'''
#check objects in bucket
for key in s3.list_objects(Bucket='lsc-tweets-finalproject')['Contents']:
    print(key['Key'])

#empty & delete bucket
s3_rec = boto3.resource('s3')
bucket = s3_rec.Bucket('lsc-tweets-finalproject')
bucket.objects.all().delete()
bucket.delete()
'''