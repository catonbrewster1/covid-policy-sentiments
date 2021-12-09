import boto3
import time
import json
import requests
import re

url = "https://427e20rcv8.execute-api.us-east-1.amazonaws.com/dev/search"

s3 = boto3.client('s3')
kinesis = boto3.client('kinesis')
shard_it = kinesis.get_shard_iterator(StreamName="twitter_stream",
                                     ShardId='shardId-000000000000',
                                     ShardIteratorType='LATEST'
                                     )["ShardIterator"]

i = 0
while True:
    print(i)
    out = kinesis.get_records(ShardIterator=shard_it,
                              Limit=1)
    for o in out['Records']:
        data = json.loads(o["Data"])
        tweet = data["tweet"]

        #remove @s, links, and non-alphanumeric characters
        tweet_clean = re.sub("@[A-Za-z0-9_]+","", tweet)
        tweet_clean = re.sub(r"http\S+", "", tweet_clean)
        tweet_clean = re.sub(r"www.\S+", "", tweet_clean)
        tweet_clean = re.sub("[^A-Za-z0-9]"," ", tweet_clean)

        # save only info we want in s3 bucket
        tweet_info = {}
        tweet_info["id"] = data["id"]
        tweet_info["tweet"] = tweet_clean
        
        #run sentiment analysis 
        payload = {
            'text': tweet_clean,
            'max': False 
        }
        response = requests.post(url, json=payload)
        ans = json.loads(response.text)
        while ans.get("message", "") == 'Endpoint request timed out':
            response = requests.post(url, json=payload)
            ans = json.loads(response.text)
        tweet_info["sentiment"] = ans
        print(ans)

        #add json file to bucket
        file_name = str(tweet_info["id"]) + ".json"
        s3.put_object(Body=json.dumps(tweet_info),
                Bucket = 'lsc-sentiments', 
                Key = file_name)

    shard_it = out['NextShardIterator']
    time.sleep(0.2)
    print('done')
    i += 1