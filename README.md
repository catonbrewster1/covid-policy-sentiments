

# Large Scale Project: Streaming COVID-19 sentiments 
Caton Brewster, Gabriela Palacios, Antonia Sanhueza


## 1. Social problem

It has been almost 2 years since Covid-19 hit the world. Since then, we have seen the virus evolve and its effects on us chance as different policies and recommentations have been issued by International Organizations, countries, states, and cities enforced and lifted. The opinions about COVID and these policies are varied: some people view constraints positively because of the care it shows while others oppose 'oppresive' policies and prefer giving people more freedom on prinicple or to maintain economic activity. In this project, we want to provide policymakers with a tool to analyze public sentiment around Covid-19 based on streaming Twitter data, so they can understand the general sentiment towards COVID while making decisions. 

In particular, we analyze the sentiments around COVID-19 using Twitter data from two cities in Mexico: Mexico City and Guadalajara. We use these cities to contrast a liberal city (Mexico City) with a more conservative city (Guadalajara) In Mexico, there have not been Federal mandates regarding quarantine and vaccines, however, each state has issued its own recommmendations and regulations.

While the scope of the project is limited by AWS Educate the Twitter API, its scaled application is valuable. Having ongoing, live access to the sentiments of your city around COVID--or a specific policy that has been introduced--would allow policy-makers to have up-to-date information on how their citizens are feeling and adapt accordingly. 


## 2. Structure of the project

Due to the enormous amount of data flowing through Twitter each day, pulling and processing that data requires additional tools designed for large scale computing. We rely on AWS for the project. Ideally, our analysis would use a Kinesis Stream to 1) pull the data from twitter using an API wrapper, 2) apply sentiment analysis using an AWS Lambda function, and 3) generate a live dashboard to visualize the sentiments using Amazon QuickSight. We outline the reality of each component below. 

#### Collecting Twitter Data
Due to limitations with the Twitter API, we simulate a streaming API instead. We use twint in [gen_data.py](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/gen_data_extended.py) to scrape data from Twitter and store it in an s3 bucket. We limit the size of data to 20 tweets per day over the course of 10 days from each city. We limit our data dramatically for two reasons: 1) twint is a glitchy the further back in time you scrape. A scaled, professional version of this project could rely on the Twitter API directly which would circumvent these problems. 2) Our Kinesis stream on AWS Educate only can access 1 shard. Thus, running our stream to process the tweets is very slow. Therefore, we limit our data so it is feasible to run everything. 

#### Kinesis Stream
We [create](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter.py) a kinesis stream and run our producer and consumer files on EC2 instances. Our [producer](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter_producer.py) pulls each object (tweet) from the bucket and sends it into the kinesis stream. The [consumer](https://github.com/catonbrewster1/covid-policy-sentiments/blob/main/twitter_consumer.py) pulls the tweets from the stream, calls the lambda function to run sentiment analysis on each tweet, and stores the tweets in another s3 bucket. 

Kinesis streams are cost efficient because with the on-demand mode you only pay for what you need. In other words, you pay for the amount of GB of data you process along with a per-hour active stream fee. See more on pricing [here](https://aws.amazon.com/kinesis/data-streams/pricing/?nc=sn&loc=3) 

#### Sentiment Analysis with lambda function
We set up the lambda function as a public url through a docker image, using AWS Elastic Container Registry. The model for sentiment analysis called in the function comes from the [Huggingface](https://huggingface.co/daveni/twitter-xlm-roberta-emotion-es?text=hola) library, which is an NLP sentiment analysis model trained on twitter data in Spanish, which is required for the location chosen. However, this could be updated to process any language, as needed.  The files for the function, except for the model and tokenizer can be found in the folder [find_emotions](https://github.com/catonbrewster1/covid-policy-sentiments/tree/main/find_emotions). 

One of the biggest benefits of using a lambda function is that it's free when not in use. When used, it costs just $0.20 per 1M requests, making it very cost-effective. The ECR is free up to 1GB and the next 9.999 TB are only $0.09 per GB per month ([Source](https://aws.amazon.com/ecr/pricing/)). Thus, the total cost of the lambda function is low in relation to other alternatives and is directly related to the size of the data we want to process.

#### Visualizing with PySpark
Due to restrictions with our AWS Educate accounts, we are unable to connect our Kinessis stream to a live dashboard using Amazon IoT and QuickSight. Therefore, our kinesis consumer stores the analyzed data in an s3 bucket. We then use PySpark on an EMR notebook to efficiently process and visualize the data. While the amount of Twitter data we use in this simulation is relatively small, we have designed a pipeline that uses tools that can be scaled as needed. 


## 4. Data

We use Twitter data from Mexico City and Guadalajara, Mexico. For the reasons outlined above, our data includes 20 daily tweets from each city over the span of 10 days (November 30th, 20201 - December 10th, 2021).


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
