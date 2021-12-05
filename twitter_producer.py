import boto3
import time
import random
import datetime
import json
import json, tweepy, time, sys, os, random

kinesis = boto3.client('kinesis', region_name='us-east-1')

#Continuously write random stock data into Kinesis stream
CONSUMER_KEY = "bzVIDZamtYW6UKOk1V7DSFThW"
CONSUMER_SECRET = "7i5cVfdKUobpMVQaz6R1RbM3hhqLuTLSf2qfTRlVd5xcR4uYHk"
ACCESS_KEY = "1467552250457473026-685etojXLSdPjZkbBrxtwo5aSKExpO"
ACCESS_SECRET = "KcPKGnpnylEZ26jivTZUC2nrRNL2CoJVpCcQED0RklP8R"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
aut.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limi=True, 
                    wait_on_rate_limit_notify=True)

SEARCH_TERMS = ["covid", 
                "covid-19", 
                "covid19", 
                "coronavirus",
                "masks", 
                "vaccine", 
                "vaccination", 
                "school closing", 
                "schoolclosing"]

def getReferrer():
    q = " OR ".join(SEARCH_TERMS)
    places = api.geo_search(query="United States", granularity="country")
    place_id = places[0].id
    ht_list_no_RT = q + " -filter:retweets"
    for tweet in tweepy.Cursor(api.search, 
                                q=(ht_list_no_RT) and ("place:%s" % place_id), 
                                tweet_mode='extended', 
                                count=100, 
                                include_entities=True,
                                lang="en").items():
                                    
        tweet_dic = tweet._json
        return tweet_dic
    

while True:
    kinesis.put_record(StreamName="twitter_stream",
                       Data=json.dumps(getReferrer()),
                       PartitionKey="partitionkey")

    