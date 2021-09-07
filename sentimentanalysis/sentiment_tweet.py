import os
import tweepy
import csv
import pandas as pd
import json

#this python script goes through the test and train datasets containing marked tweets based on positive, negative and neutral sentiment and then puts them in a format that will then be used to train a sentiment analysis model.


consumer_key = "783ZxxFfcUkh4y5eG88JtgVG0"
consumer_secret = "10JlCd50Hpw0yICiTsHnYgNfcdiQGKxtDMM8ZRnpNsASPVHmug"
access_token = "921665261853466624-sYD4ZDpFA8CNHyeeKKwL2ZA1wwLrBtp"
access_token_secret = "TFRNyf6zlsvkKGi1j91bPdPr9LpRZ42Ta0TG7SLXlPmrm"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)



positive_test_dataf = {
"id": "",
"sentence": "",
"value": ""
}

notr_test_dataf = {
"id": "",
"sentence": "",
"value": ""
}
negative_test_arr = []
positive_test_arr = []
notr_test_arr = []

with open('negative-train') as f:
    lines = f.readlines()
    for line in lines:
        try:
            tweet = api.get_status(id=line[:-1])
        except tweepy.errors.NotFound:
            continue
        except tweepy.errors.Forbidden:
            continue
        except tweepy.errors.TweepyException:
            continue
        negative_test_dataf = {
        "id": "",
        "sentence": "",
        "value": ""
        }
        negative_test_dataf["id"] = line
        negative_test_dataf["sentence"] = tweet.text
        negative_test_dataf["value"] = "negative"
        negative_test_arr.append(negative_test_dataf)

 
with open('positive-train') as f:
     lines = f.readlines()
     for line in lines:
         try:
             tweet = api.get_status(id=line[:-1])
         except tweepy.errors.NotFound:
             continue
         except tweepy.errors.Forbidden:
             continue
         except tweepy.errors.TweepyException:
             continue
         negative_test_dataf = {
         "id": "",
         "sentence": "",
         "value": ""
         }
         negative_test_dataf["id"] = line
         negative_test_dataf["sentence"] = tweet.text
         negative_test_dataf["value"] = "positive"
         negative_test_arr.append(negative_test_dataf)

with open('notr-train') as f:
     lines = f.readlines()
     for line in lines:
         try:
             tweet = api.get_status(id=line[:-1])
         except tweepy.errors.NotFound:
             continue
         except tweepy.errors.Forbidden:
             continue
         except tweepy.errors.TweepyException:
             continue
         negative_test_dataf = {
         "id": "",
         "sentence": "",
         "value": ""
         }
         negative_test_dataf["id"] = line
         negative_test_dataf["sentence"] = tweet.text
         negative_test_dataf["value"] = "notr"
         negative_test_arr.append(negative_test_dataf)
 

print(negative_test_arr)

#train.json is the train dataset that will be used to train the model
with open('train.json', 'w') as outfile:
    json.dump(negative_test_arr, outfile)


negative_test_arr = []
positive_test_arr = []
notr_test_arr = []

with open('negative-test') as f:
    lines = f.readlines()
    for line in lines:
        try:
            tweet = api.get_status(id=line[:-1])
        except tweepy.errors.NotFound:
            continue
        except tweepy.errors.Forbidden:
            continue
        except tweepy.errors.TweepyException:
            continue
        negative_test_dataf = {
        "id": "",
        "sentence": "",
        "value": ""
        }
        negative_test_dataf["id"] = line
        negative_test_dataf["sentence"] = tweet.text
        negative_test_dataf["value"] = "negative"
        negative_test_arr.append(negative_test_dataf)

 
with open('positive-test') as f:
     lines = f.readlines()
     for line in lines:
         try:
             tweet = api.get_status(id=line[:-1])
         except tweepy.errors.NotFound:
             continue
         except tweepy.errors.Forbidden:
             continue
         except tweepy.errors.TweepyException:
             continue
         negative_test_dataf = {
         "id": "",
         "sentence": "",
         "value": ""
         }
         negative_test_dataf["id"] = line
         negative_test_dataf["sentence"] = tweet.text
         negative_test_dataf["value"] = "positive"
         negative_test_arr.append(negative_test_dataf)

with open('notr-test') as f:
     lines = f.readlines()
     for line in lines:
         try:
             tweet = api.get_status(id=line[:-1])
         except tweepy.errors.NotFound:
             continue
         except tweepy.errors.Forbidden:
             continue
         except tweepy.errors.TweepyException:
             continue
         negative_test_dataf = {
         "id": "",
         "sentence": "",
         "value": ""
         }
         negative_test_dataf["id"] = line
         negative_test_dataf["sentence"] = tweet.text
         negative_test_dataf["value"] = "notr"
         negative_test_arr.append(negative_test_dataf)
 

print(negative_test_arr)

#test.json contains the data that will be used to test the model.
with open('test.json', 'w') as outfile:
    json.dump(negative_test_arr, outfile)
