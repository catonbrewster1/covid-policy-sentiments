Caton Brewster

Gabriela Palacios

Antonia Sanhueza

# Large Scale Project: Analyzing sentiment around COVID-19 policies



## 1. Social problem

It has been almost 2 years since Covid-19 hit the world. Since then, we have seen many different policies at the country, state, city and community level enforced and lifted as the virus and contagions change. The opinions around these policies are varied, some are happy when there are more constraints and being more careful, other oppose 'oppresive' policies and rather give people more freedom. In this project, we want to provide policymakers with a tool  to analyze public sentiment around such policies based on Twitter data.  

In particular, we will be pulling data from Santiago, Chile as the Covid-19 measures for each municipality are announced on a weekly basis based on a 5 stage model.  Every week the Ministry of Health announces which municipalities will move forward, go back or remain the same.  That means that from one week to another people have to be on lock down, or your 200 people wedding has to be reduced to 50, you don't know what they are going to announce. 



## 2. Serial Computation Bottlenecks

If we did everything serially it would take a long time? should we be talking O(n)?? If the kinesis has n workers processing m amount of data, then the serial implementation would be mxn times that of the parallel implementation. We reach a bottleneck once the data is actually turned into a visualization since we need to aggregate it.

## 3. Structure of the project

We wanted to set up a Kinesis Stream that would pull the data from twitter, generate the sentiment analysis, and store this information to later produce a visualization where information would be provided in a clear and simple way.

Due to the limited access we have to twitter data, we simulate a streaming API by using twint to pull data from Twitter into an s3 bucket. Then, we [set up](file) a kinesis stream where our [producer](file) pulls each object (tweet) from the bucket and sends them into the kinesis. The [consumer](file), calls a lambda function that produces the sentiment analysis and stores the analyzed data into another s3 bucket (or updates de record in the preivous?). Later, we use this information to set up a visualization where we can easily observe the general sentiment of the population through time. TALK ABOUT COST OF KINESIS

We set up the lambda function as a public url through a docker image, using AWS Elastic Container Registry. The model for sentiment analysis called in the function comes from the [Huggingface](https://huggingface.co/daveni/twitter-xlm-roberta-emotion-es?text=hola) library, it is an NLP sentiment analysis model trained on twitter data in Spanish, which we require for the location chosen. However, this could be done using an english model or any other language, if we wanted to implement it for other countries/regions.  The files for the function, expcept for the model an tokenizer can be found in the folder [find_emotions](folder). One of the biggest benefits of using this lambda call is that when not in use is almost free, and even when we call it it's just $$$ so it is a very efficient way of doing sentiment analysis in AWS.



## 4. Data

Our data are tweets from users of Santiago, Chile between DATE and DATE. 



## 5. Results

## 6. References



### * initial proposal

For our project, we proposed to analyze the psychological effects on the public of policies associated with COVID-19 over the past year. We will choose several cities and/or states and track major changes in policies related to travel, masks, vaccines, and school closings. Following major changes to these policies, we will analyze public sentiment on Twitter related toward various COVID-related concepts. We will also explore whether there is heterogeneity in the responses based on political majorities. We think this analysis may help to understand any negative externalities of policies on public wellbeing and opinions which may ultimately affect their compliance in unexpected ways. We plan to use AWS services to perform our data processing and analysis. We will find data related to COVID policies over time. We will use the Twitter API to get Twitter data and use an EMR cluster to clean the data, parallelize the twitter’s sentiment analysis, and aggregate it by building an overall sentiment index of the determined concept. We plan to use AWS comprehend and/or upload a huggingface model to an EC2 or lambda to do the NLP analysis.Our tentative timeline is as follows:

