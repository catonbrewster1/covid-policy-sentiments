# covid-policy-sentiments
Explore Twitter sentiments on COVID-19 in response to various state-level executive orders

For our project, we plan to analyze the psychological effects on the public of policies associated with COVID-19 over the past year. We will choose several cities and/or states and track major changes in policies related to travel, masks, vaccines, and school closings. Following major changes to these policies, we will analyze public sentiment on Twitter related toward various COVID-related concepts. We will also explore whether there is heterogeneity in the responses based on political majorities. We think this analysis may help to understand any negative externalities of policies on public wellbeing and opinions which may ultimately affect their compliance in unexpected ways. We plan to use AWS services to perform our data processing and analysis. We will find data related to COVID policies over time. We will use the Twitter API to get Twitter data and use an EMR cluster to clean the data, parallelize the twitter’s sentiment analysis, and aggregate it by building an overall sentiment index of the determined concept. We plan to use AWS comprehend and/or upload a huggingface model to an EC2 or lambda to do the NLP analysis.

Our tentative timeline is as follows:
* Week 15- 19 Nov. Exploratory analysis of data. Get a subset of the data and perform EMR operations to familiarize ourselves with the results we might be able to get and conclusions we can derive.
* Caton: get Twitter data
* Gaby: get policies data
* Antonia: research NLP models
* All together: test out and finalize our NLP sentiment analysis models on smaller scale data

Week 29 Nov - 3 Dec. Align on final metrics of interest for analysis. Scale analysis to data from multiple states and/or cities.
* All together: align on metrics together and ensure our models still work on larger scale data

Week 6 Dec - 10 Dec. Create visualizations and summarize findings
* Depending on the number of and style of visualizations, we will divide creating those amongst the three of us and also each write a different portion of the write-up.
