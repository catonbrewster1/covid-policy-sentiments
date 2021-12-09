import boto3
import time
import random
import datetime
import json
import twint
import nest_asyncio
nest_asyncio.apply()

kinesis = boto3.client('kinesis', region_name='us-east-1')

#Continuously write random stock data into Kinesis stream
#CONSUMER_KEY = "bzVIDZamtYW6UKOk1V7DSFThW"
#CONSUMER_SECRET = "7i5cVfdKUobpMVQaz6R1RbM3hhqLuTLSf2qfTRlVd5xcR4uYHk"
#ACCESS_KEY = "1467552250457473026-685etojXLSdPjZkbBrxtwo5aSKExpO"
#ACCESS_SECRET = "KcPKGnpnylEZ26jivTZUC2nrRNL2CoJVpCcQED0RklP8R"

SEARCH_TERMS = ["covid", 
                "covid-19", 
                "covid19", 
                "coronavirus",
                "masks", 
                "vaccine", 
                "vaccination", 
                "school closing", 
                "schoolclosing"]

c = twint.Config()
c.Search = "covid"
c.Pandas = True
c.Limit = 20
c.Hide_output = True
twint.run.Search(c) 
df = twint.storage.panda.Tweets_df
df_dict = df.to_dict()
while True:

    kinesis.put_record(StreamName="twitter_stream",
                       Data=json.dumps(df_dict),
                       PartitionKey="partitionkey")

    