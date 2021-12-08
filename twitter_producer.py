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
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

SEARCH_TERMS = ['covid', 'avanzan', 'apertura', 'retroceden']
# SEARCH_TERMS = ["covid", 
#                 "covid-19", 
#                 "covid19", 
#                 "coronavirus",
#                 "masks", 
#                 "vaccine", 
#                 "vaccination", 
#                 "school closing", 
#                 "schoolclosing"]

def getReferrer():
    q = " OR ".join(SEARCH_TERMS)
    #places = api.search_geo(query="Chile", granularity="country")
    #place_id = places[0].id
    ht_list_no_RT = q + " -filter:retweets"
    for tweet in tweepy.Cursor(api.search, 
                                q=ht_list_no_RT, 
                                geo='-33.447487, -70.673676, 100',
                                tweet_mode='extended', 
                                count=100, 
                                include_entities=True,
                                lang="es").items()[:10]:
                                    
        tweet_dic = tweet._json
        print('tweet_dic')
        return tweet_dic
    

while True:
    kinesis.put_record(StreamName="twitter_stream",
                       Data=json.dumps(getReferrer()),
                       PartitionKey="partitionkey")

    