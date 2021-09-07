from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

consumer_key = "783ZxxFfcUkh4y5eG88JtgVG0"
consumer_secret = "10JlCd50Hpw0yICiTsHnYgNfcdiQGKxtDMM8ZRnpNsASPVHmug"
access_key = "921665261853466624-sYD4ZDpFA8CNHyeeKKwL2ZA1wwLrBtp"
access_secret = "TFRNyf6zlsvkKGi1j91bPdPr9LpRZ42Ta0TG7SLXlPmrm"
           
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def percentage(part,whole):
    return 100 * float(part)/float(whole)



  
# function to perform data extraction
def scrape(words, date_since, numtweet):
      
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])
      
    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    #tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en").items(numtweet)
    words = "#" + words
    tweets = tweepy.Cursor(api.search_tweets, q=(words)).items(numtweet)
    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]
      
    # Counter to maintain Tweet Count
    i = 1
      
    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
          
        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
      #  try:
      #      text = tweet.retweeted_status.full_text
      #  except AttributeError:
      #
        text = tweet.text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
          
        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet
          
        # Function call to print tweet data on screen
        #printtweetdata(i, ith_tweet)
        i = i+1
    filename = 'scraped_tweets.csv'
      
    # we will save our database as a CSV file.
    db.to_csv(filename)


#function for the english sentiment analysis using the existing library module sentiment analyzer
def analyze():
    consumer_key = "783ZxxFfcUkh4y5eG88JtgVG0"
    consumer_secret = "10JlCd50Hpw0yICiTsHnYgNfcdiQGKxtDMM8ZRnpNsASPVHmug"
    access_key = "921665261853466624-sYD4ZDpFA8CNHyeeKKwL2ZA1wwLrBtp"
    access_secret = "TFRNyf6zlsvkKGi1j91bPdPr9LpRZ42Ta0TG7SLXlPmrm"
               
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
                 
               # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()
               #print("Enter Date since The Tweets are required in yyyy-mm--dd")
    date_since = "xx"
                 
               # number of tweets you want to extract in one run
    print("Enter the number of tweets to search for")
    num = input()
    # number of tweets you want to extract in one run
    numtweet = int(num)
            #   tweets = tweepy.Cursor(api.search,q=words,count=100, lang="en", since=date_since).items(numtweet)
    scrape(words, date_since, numtweet)
    print('Scraping has completed!')


    dataset = pd.read_csv("scraped_tweets.csv")
    #dataset['value'] = 0

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    
    location = 0
    for tweet in dataset["text"]:
     
     #print(tweet.text)
         tweet_list.append(tweet)
         analysis = TextBlob(tweet)
         score = SentimentIntensityAnalyzer().polarity_scores(tweet)
         neg = score['neg']
         neu = score['neu']
         pos = score['pos']
         comp = score['compound']
         polarity += analysis.sentiment.polarity
         
         if neg > pos:
             dataset.at[location,"value"] = "-1"
             #dataset.iloc[location, 11] = -1
             negative_list.append(tweet)
             negative += 1
         elif pos > neg:
             dataset.at[location,"value"] = "1"
             #dataset.iloc[location, 11] = 1
             positive_list.append(tweet)
             positive += 1
         
         elif pos == neg:
             dataset.at[location,"value"] = "0"
             #dataset.iloc[location, 11] = 0
             neutral_list.append(tweet)
             neutral += 1
         location = location + 1
    noOfTweet = len(dataset.index) - 1

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)
    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')

    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    print("total number: ",len(tweet_list))
    print("positive number: ",len(positive_list))
    print("negative number: ", len(negative_list))
    print("neutral number: ",len(neutral_list))


    dataset.to_csv('output.csv')
