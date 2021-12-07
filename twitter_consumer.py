import boto3
import time
import json
from transformers import pipeline
import sagemaker
from sagemaker.huggingface.model import HuggingFaceModel


data = {
  "created_at": "Thu Jun 22 21:00:00 +0000 2017",
  "id": 877994604561387500,
  "id_str": "877994604561387520",
  "text": "Creating a Grocery List Manager Using Angular, Part 1: Add &amp; Display Items https://t.co/xFox78juL1 #Angular",
  "truncated": False,
  "entities": {
    "hashtags": [{
      "text": "Angular",
      "indices": [103, 111]
    }],
    "symbols": [],
    "user_mentions": [],
    "urls": [{
      "url": "https://t.co/xFox78juL1",
      "expanded_url": "http://buff.ly/2sr60pf",
      "display_url": "buff.ly/2sr60pf",
      "indices": [79, 102]
    }]
  },
  "source": "<a href=\"http://bufferapp.com\" rel=\"nofollow\">Buffer</a>",
  "user": {
    "id": 772682964,
    "id_str": "772682964",
    "name": "SitePoint JavaScript",
    "screen_name": "SitePointJS",
    "location": "Melbourne, Australia",
    "description": "Keep up with JavaScript tutorials, tips, tricks and articles at SitePoint.",
    "url": "http://t.co/cCH13gqeUK",
    "entities": {
      "url": {
        "urls": [{
          "url": "http://t.co/cCH13gqeUK",
          "expanded_url": "https://www.sitepoint.com/javascript",
          "display_url": "sitepoint.com/javascript",
          "indices": [0, 22]
        }]
      },
      "description": {
        "urls": []
      }
    },
    "protected": False,
    "followers_count": 2145,
    "friends_count": 18,
    "listed_count": 328,
    "created_at": "Wed Aug 22 02:06:33 +0000 2012",
    "favourites_count": 57,
    "utc_offset": 43200,
    "time_zone": "Wellington",
  },
}


kinesis = boto3.client('kinesis', region_name='us-east-1')
shard_it = kinesis.get_shard_iterator(StreamName="twitter_stream",
                                     ShardId='shardId-000000000000',
                                     ShardIteratorType='LATEST'
                                     )["ShardIterator"]


while True:

    out = kinesis.get_records(ShardIterator=shard_it,
                              Limit=1)
    for i, o in enumerate(out['Records']):
        data = json.loads(o["Data"])
        #get the names of the variables we want to run sentiment analysis on
        tweet = data["text"]
        #data["sentiment"] 
        print(tweet)
        #add json file to bucket
        file_name = data["id_str"] + ".json"
        s3.put_object(Body=json.dumps(data),
                  Bucket = 'lsc-project', 
                  Key = file_name)
        if i == 100: 
          break

    shard_it = out['NextShardIterator']
    time.sleep(0.2)
    predictor.delete_endpoint()