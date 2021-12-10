

# Large Scale Project: Streaming COVID-19 sentiments 
Caton Brewster, Gabriela Palacios, Antonia Sanhueza


## 1. Social problem

It has been almost 2 years since Covid-19 hit the world. Since then, we have seen many different policies and recommentations issued by International Organizations, countries, states, and cities enforced and lifted as the virus and contagions change. The opinions around these policies are varied, some are positive when there are more constraints and being more careful, other oppose 'oppresive' policies and rather give people more freedom and allow for economic recovery. In this project, we want to provide policymakers with a tool to analyze public sentiment around Covid-19 based on Twitter data, so they can take better and informed decisiones about future policies.  

In particular, we will use data from two cities in Mexico: Mexico City and Guadalajara. We chose these cities to contrast a liberal city such as Mexico City, and Guadalajara, which is more conservative. In Mexico there has not been Federal mandatory policies regarding quarantine and vaccines, however each state has issued its recommmendations and shut down firms in non essential economic activities.


## 2. Structure of the project

Due to the enormous amount of data flowing through Twitter each day, pulling and processing that data requires additional tools designed for large scale computing. We rely on AWS for the project. Ideally, our analysis would use a Kinesis Stream to 1) pull the data from twitter using an API wrapper, 2) apply sentiment analysis using an AWS Lambda function, and 3) generate a live dashboard to visualize the sentiments using Amazon QuickSight. 

#### Collecting Twitter Data
Due to limitations with the Twitter API, we instead simulate a streaming API. We use twint in [gen_data.py](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/gen_data_extended.py) to scrape data from Twitter and store it in an s3 bucket. We limit the size of data to 20 tweets per day over theh past 10 days from each city. We limit our data dramatically for two reasons: 1) twint is a glitchy the further back in time you scrape. A scaled, professional version of this project could relying on the Twitter API directly which would circumvent these problems. 2) Our Kinesis stream on AWS Educate only can access 1 shard. Thus, running our stream to process the tweets was very slow. Therefore, we limited our data so it was feasible to run everything. 

#### Kinesis Stream
We [create](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter.py) a kinesis stream and run our producer and consumer files on EC2 instances. Our our [producer](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter_producer.py) pulls each object (tweet) from the bucket and sends it into the kinesis stream. The [consumer](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter_consumer.py), pulls the tweets from the stream, and calls the lambda function that applies a sentiment analysis model. 

Kinesis streams are also cost efficient because with the on-demand mode you only pay for what you need. In other words, you pay for the amount of GB of data you process along with a per-hour active stream fee. See more on pricing [here](https://aws.amazon.com/kinesis/data-streams/pricing/?nc=sn&loc=3) 

#### Sentiment Analysis with lambda function
We set up the lambda function as a public url through a docker image, using AWS Elastic Container Registry. The model for sentiment analysis called in the function comes from the [Huggingface](https://huggingface.co/daveni/twitter-xlm-roberta-emotion-es?text=hola) library, which is an NLP sentiment analysis model trained on twitter data in Spanish, which we require for the location chosen. However, this could be done using an english model or any other language, if implemented in other countries/regions.  The files for the function, expcept for the model and tokenizer can be found in the folder [find_emotions](https://github.com/catonbrewster1/covid-policy-sentiments/tree/main/find_emotions). 

One of the biggest benefits of using this lambda call is that when not in use it's free, and even when called it is just $0.20 per 1M requests, making it very cost-effective. The ECR is free up to 1GB and the next 9.999 TB are only $0.09 per GB per month ([Source](https://aws.amazon.com/ecr/pricing/)). Thus, the total cost of the lambda function is low in relation to other alternatives, and directly related to the size of the data we want to process.

#### Visualizing with PySpark
Due to restrictions with our AWS Educate accounts, we are unable to connect our Kinessis stream to a live dashboard using Amazon IoT and Amazon QuickSight. Therefore, our kinesis consumer stores the analyzed data an s3 bucket. We then use PySpark on EMR notebook to efficiently process and visualize the data. While the amount of Twitter data we use in this simulation is relatively small, we have designed a pipeline that uses tools that can be scaled as needed. 


## 4. Data

Our sample has Twitter data from Mexico City and Guadalajara, Mexico. For the reasons outlined above, we have pulled 20 daily tweets from each city over the span of 10 days (November 30th, 20201 - December 10th, 2021).


## 5. Results

## 6. How to run the project

The following are the steps to simulate what we did:
1) Run [gen_data_mini.py](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/gen_data_mini.py) to generate the initial s3 bucket with the twitter data
2) Run the kinesis stream using the [twitter.py](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter.py) file. For the file to run correctly, you need to add your personal security group id, pem key name, and pem key file name as stated in the line 14-20.
3) Use the pyspark notebook to produce the visualization[https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/visualization.ipynb]

## 6. References


## 6. Team responsibilities

The main tasks and team members involved in each one are the following:

- Using Docker to push the NLP model into a lambda function and deploy the lambda function - Antonia Sanhueza and Gabriela Palacios
- Kinesis Stream - All
- Visualization - Gabriela Palacios and Caton Brewster
- ReadMe - All