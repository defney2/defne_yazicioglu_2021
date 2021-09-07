import pandas as pd
import tweepy
from sentiment4 import analyzer
from sentimentanalysis import scrape
from sentimentanalysis import analyze

#interface for the sentiment analysis on tweets
def main():
    print("Enter the language of tweets you want to search - options: eng, tr")
    words = input()
    while (words != "tr" and words != "eng"):
        print("Enter the language of tweets you want to search - options: eng, tr")
        words = input()
        
    if words == "tr":
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
        analyzer()
    
    else:
        analyze()
        



if __name__ == '__main__':
    main()
     
     
         
