

# Large Scale Project: Streaming COVID-19 sentiments 
Caton Brewster, Gabriela Palacios, Antonia Sanhueza


## 1. Social problem

It has been almost 2 years since Covid-19 hit the world. Since then, we have seen many different policies at the country, state, city and community level enforced and lifted as the virus and contagions change. The opinions around these policies are varied, some are happy when there are more constraints and being more careful, other oppose 'oppresive' policies and rather give people more freedom. In this project, we want to provide policymakers with a tool  to analyze public sentiment around such policies based on Twitter data.  

In particular, we will be pulling data from Santiago, Chile as the Covid-19 measures for each municipality are announced on a weekly basis based on a 5 stage model.  Every week the Ministry of Health announces which municipalities will move forward, go back or remain the same.  That means that from one week to another people have to be on lock down, or your 200 people wedding has to be reduced to 50, you don't know what they are going to announce. 

## 2. Structure of the project

Due to the enormous amount of data flowing through Twitter each day, pulling and processing that data requires additional tools designed for large scale computing. We rely on AWS for the project. Ideally, our analysis would use a Kinesis Stream to 1) pull the data from twitter using an API wrapper, 2) apply sentiment analysis using an AWS Lambda function, and 3) generate a live dashboard to visualize the sentiments using Amazon QuickSight. 

#### Collecting Twitter Data
Due to limitations with the Twitter API, we instead simulate a streaming API. We use twint in [gen_data.py](file) to scrape data from Twitter and store it in an s3 bucket. We limit our data to PUT IN DETAILS OF OUR FINAL DATASET HERE. 

#### Kinesis Stream
Then, we [create](file) a kinesis stream where our [producer](file) pulls each object (tweet) from the bucket and sends them into the kinesis stream. The [consumer](file), pulls the tweets from the stream, calls a lambda function that applies a sentiment analysis model. 

TALK ABOUT COST OF KINESIS

#### Sentiment Analysis with lambda function
We set up the lambda function as a public url through a docker image, using AWS Elastic Container Registry. The model for sentiment analysis called in the function comes from the [Huggingface](https://huggingface.co/daveni/twitter-xlm-roberta-emotion-es?text=hola) library, it is an NLP sentiment analysis model trained on twitter data in Spanish, which we require for the location chosen. However, this could be done using an english model or any other language, if we wanted to implement it for other countries/regions.  The files for the function, expcept for the model an tokenizer can be found in the folder [find_emotions](folder). One of the biggest benefits of using this lambda call is that when not in use is almost free, and even when we call it it's just $$$ so it is a very efficient way of doing sentiment analysis in AWS.

#### Visualizing with PySpark
Due to restrictions with our AWS Educate accounts, we are unable to connect our Kinessis stream to a live dashboard using Amazon IoT and Amazon QuickSight. Therefore, our kinesis consumer stores the analyzed data an s3 bucket. We then use PySpark on EMR notebook to efficiently process and visualize the data. While the amount of Twitter data we use in this simulation is relatively small, we have designed a pipeline using tools that can be scaled as needed. 



## 4. Data

Our data are tweets from users of Santiago, Chile between DATE and DATE. 



## 5. Results

## 6. References



### * initial proposal

For our project, we proposed to analyze the psychological effects on the public of policies associated with COVID-19 over the past year. We will choose several cities and/or states and track major changes in policies related to travel, masks, vaccines, and school closings. Following major changes to these policies, we will analyze public sentiment on Twitter related toward various COVID-related concepts. We will also explore whether there is heterogeneity in the responses based on political majorities. We think this analysis may help to understand any negative externalities of policies on public wellbeing and opinions which may ultimately affect their compliance in unexpected ways. We plan to use AWS services to perform our data processing and analysis. We will find data related to COVID policies over time. We will use the Twitter API to get Twitter data and use an EMR cluster to clean the data, parallelize the twitter’s sentiment analysis, and aggregate it by building an overall sentiment index of the determined concept. We plan to use AWS comprehend and/or upload a huggingface model to an EC2 or lambda to do the NLP analysis.Our tentative timeline is as follows:

