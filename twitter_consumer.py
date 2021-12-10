import boto3
import time
import json
import requests
import re

BUCKET_NAME = 'lsc-sentiments'
lambda_url = "https://427e20rcv8.execute-api.us-east-1.amazonaws.com/dev/search"

s3 = boto3.client('s3')
kinesis = boto3.client('kinesis')
shard_it = kinesis.get_shard_iterator(StreamName="twitter_stream",
                                     ShardId='shardId-000000000000',
                                     ShardIteratorType='LATEST'
                                     )["ShardIterator"]

def clean_results(text, emotions_dict):
    split_emotions = re.split('\) +', text[3:])
    emotions_dict['anger'] = 0
    emotions_dict['disgust'] = 0
    emotions_dict['fear'] = 0
    emotions_dict['surprise'] = 0
    emotions_dict['joy'] = 0
    
    for emotion in split_emotions:
        e = emotion.split()
        emotions_dict[e[0]] = e[1]

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
        tweet_info["tweet"] = data["tweet"]
        tweet_info["date"] = data["date"]
        tweet_info["geo"] = data["geo"]
        
        #run sentiment analysis 
        payload = {
            'text': tweet_clean,
            'max': False 
        }
        response = requests.post(lambda_url, json=payload)
        ans = json.loads(response.text)
        while ans.get("message", "") == 'Endpoint request timed out':
            response = requests.post(lambda_url, json=payload)
            ans = json.loads(response.text)
        tweet_info["sentiment"] = ans
        if ('error' in ans) or ('message' in ans):
            print('error is in answer', 'error' in ans)
            continue
        print(ans)    

        #add clean tweet info to bucket
        clean_results(ans['results'], tweet_info)
        file_name = str(tweet_info["id"]) + ".json"
        s3.put_object(Body=json.dumps(tweet_info),
                Bucket = BUCKET_NAME, 
                Key = file_name)

    shard_it = out['NextShardIterator']
    time.sleep(0.2)
    print('done')
    i += 1