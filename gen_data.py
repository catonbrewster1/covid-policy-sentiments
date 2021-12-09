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

kinesis = boto3.client('kinesis', region_name='us-east-1')
s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket='lsc-tweets')

SEARCH_TERMS = ["covid", 
                "covid-19", 
                "covid19", 
                "coronavirus",
                "masks", 
                "vaccine", 
                "vaccination", 
                "school closing", 
                "schoolclosing"]

'''#get data over last year
start_date = date(2020, 12, 1)
stop_date = date(2021, 12, 1)

def daterange(start_date, stop_date):
    for n in range(int((stop_date - start_date).days)):
        date = start_date + timedelta(n)
        yield date.strftime("%Y-%m-%d")

for end_date in daterange(start_date, stop_date):
print("Date: ", end_date)
'''

c = twint.Config()
c.Search = "covid"
c.Pandas = True
c.Limit = 1000
#c.Until = end_date
#c.Hide_output = True
twint.run.Search(c) 
df = twint.storage.panda.Tweets_df
print(len(df.index))
df_dict = df.to_dict('index')
serialized_dict = pickle.dumps(df_dict)
if df_dict: 
    file_name = "tweets.json"

    response = s3.put_object(Bucket='lsc-tweets', Key=file_name, Body=serialized_dict)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")
else: 
    print("not added")



'''
#check objects in bucket
for key in s3.list_objects(Bucket='lsc-tweets')['Contents']:
    print(key['Key'])

#empty & delete bucket
s3_rec = boto3.resource('s3')
bucket = s3_rec.Bucket('lsc-tweets')
bucket.objects.all().delete()
bucket.delete()
'''