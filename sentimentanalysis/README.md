The sentimentanalysis project scrapes tweets containing a specific hashtag from Twitter and performs sentiment analysis on those tweets to categorize them as positive, negative or neutral.

The files "positive-train", "positive-test", "negative-train", "negative-test", "notr-test" and "notr-train" are the files containing IDs of Turkish tweets tagged as positive, negative or neutral.

The "sentiment_tweet.py" file goes through the test and train datasets and scrapes the tweet IDs to get the text of each tweet. Then these tweets are placed in two dataframes "train.json" and "test.json".

The hashtag.py file is the interface where the user can enter the language they want to run the sentiment analysis in ("eng" for english or "tr" for turkish) as well as the hashtag they want to search for and the number of tweets they want to scrape. 
The scrape() function from the python script "sentimentanalysis.py" is used to scrape tweets from twitter according to the hashtag and the number of tweets inputted by the user. The output is a database containing the tweets "scraped_tweets.csv".

If the selected language is english then the analyze() function from the "sentimentanalysis.py" python script is called, which uses the existing module SentimentIntensityAnalyzer().polarity_scores() to conduct sentiment analysis on the tweets in "scraped_tweets.csv".
The output of the function is the number of tweets that are positive, negative and neutral as well as the file "output.csv" which is identical to "scraped_tweets.csv"  with an additional column "value" that indicates the output of the sentiment analysis for each tweet. -1: negative, +1: positive, 0: neutral

If the selected language is Turkish then the analyzer() function from the "sentiment4.py" python script is called, which uses the pretrained BERT model "dbmdz/bert-base-turkish-128k-uncased" as well as the "train.json" and "test.json" databases to conduct sentiment analysis on the tweets in "scraped_tweets.csv".
The output of the function is the number of tweets that are positive, negative and neutral as well as the file "output.csv" which is identical to "scraped_tweets.csv"  with an additional column "value" that indicates the output of the sentiment analysis for each tweet. -1: negative, +1: positive, 0: neutral



