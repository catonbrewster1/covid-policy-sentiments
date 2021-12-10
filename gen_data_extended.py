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

bucket_name = 'lsc-tweets'
kinesis = boto3.client('kinesis', region_name='us-east-1')
s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket=bucket_name)

SEARCH_TERMS = ["covid", 
                "covid-19", 
                "covid19", 
                "coronavirus"]
QUERY = " OR ".join(SEARCH_TERMS)

start_date = date(2021, 11, 30)
stop_date = date(2021, 12, 11)

def daterange(start_date, stop_date):
    for n in range(int((stop_date - start_date).days)):
        date = start_date + timedelta(n+1)
        yield date.strftime("%Y-%m-%d")

dates =  list(daterange(start_date, stop_date))
dates.reverse()

geo_dict = {"CDMX": "19.4326, -99.1332, 20km", 
            "GDL": "20.6597, -103.3496, 20km"}

# scrape 20 tweets each day over 10 days 
# in Mexico City and Guadalajara
for loc in geo_dict.keys():
    for end_date in dates:
        print("Date: ", end_date)
        c = twint.Config()
        c.Search = QUERY
        c.Lang = "es"
        c.Geo = geo_dict[loc]
        c.Pandas = True
        c.Limit = 20
        c.Until = end_date
        c.Hide_output = True
        df = None
        while df is None:
            try:
                twint.run.Search(c)
                df = twint.storage.panda.Tweets_df 
            except:
                pass
        print(len(df))
        if len(df) > 0:
            df_dict = df.to_dict('index')
            serialized_dict = pickle.dumps(df_dict)
            file_name = loc + "_" + end_date + ".json"
            print(file_name)
            response = s3.put_object(Bucket=bucket_name, Key=file_name, Body=serialized_dict)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status == 200:
                print(f"Successful S3 put_object response. Status - {status}")
            else:
                print(f"Unsuccessful S3 put_object response. Status - {status}")
        else: 
            print("didn't add")
        time.sleep(10)


'''
for end_date in dates:
    obj = s3.get_object(Bucket=bucket_name, Key=end_date + ".json")
    obj_ser = obj["Body"].read()
    data = pickle.loads(obj_ser)
    break


#check objects in bucket
for key in s3.list_objects(Bucket=bucket_name)['Contents']:
    print(key['Key'])

#empty & delete bucket
s3_rec = boto3.resource('s3')
bucket = s3_rec.Bucket(bucket_name)
bucket.objects.all().delete()
bucket.delete()
'''