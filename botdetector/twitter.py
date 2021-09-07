import os
import tweepy
import csv
import pandas as pd
from datetime import datetime, timezone



consumer_key = "783ZxxFfcUkh4y5eG88JtgVG0"
consumer_secret = "10JlCd50Hpw0yICiTsHnYgNfcdiQGKxtDMM8ZRnpNsASPVHmug"
access_token = "921665261853466624-sYD4ZDpFA8CNHyeeKKwL2ZA1wwLrBtp"
access_token_secret = "TFRNyf6zlsvkKGi1j91bPdPr9LpRZ42Ta0TG7SLXlPmrm"


#this function is used to go through the datasets containing users and information on whether they are bots and saves their scraped user information using the tweepy module

def teach_easy_model():
    #establishes the dataframe where the scraped information will be saved
    dataf = {
            'statuses_count': [],
            'followers_count': [],
            'friends_count': [],
            'favourites_count': [],
            'listed_count': [],
            'default_profile': [],
            'profile_use_background_image': [],
            'verified': [],
            'tweet_freq': [],
            'followers_growth_rate': [],
            'friends_growth_rate': [],
            'favourites_growth_rate': [],
            'listed_growth_rate': [],
            'followers_friend_ratio': [],
            'screenname_length': [],
            'num_digits_in_screenname': [],
            'name_length': [],
            'name_digits_in_name': [],
            'description_length': [],
            'isbot': []
            }
            
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    filelist = ["celebrity-2019.tsv", "botwiki-2019.tsv", "cresci-stock-2018.tsv",  "verified-2019.tsv", "political-bots-2019.tsv", "midterm-2018.tsv", "pronbots-2019.tsv", "crowdflower_results_detailed.tsv", "gilani-2017.tsv", "botometer-feedback-2019.tsv", "cresci-rtbust-2019.tsv", "vendor-purchased-2019.tsv"]
    
    #loops through the dataset files to scrape the user info in each
    for file in filelist:
        tsv_file = open(file)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        
        for row in read_tsv:
            try:
                user = api.get_user(user_id=row[0])
            except tweepy.errors.NotFound:
                continue
            except tweepy.errors.Forbidden:
                continue
            except tweepy.errors.TweepyException:
                continue
            
            screenname = user.screen_name
            name = user.name
            dataf['statuses_count'].append(user.statuses_count)
            dataf['followers_count'].append(user.followers_count)
            dataf['friends_count'].append(user.friends_count)
            dataf['favourites_count'].append(user.favourites_count)
            dataf['listed_count'].append(user.listed_count)
            dataf['default_profile'].append(user.default_profile)
            dataf['profile_use_background_image'].append(user.profile_use_background_image)
            dataf['verified'].append(user.verified)
            
            current_time = datetime.now(timezone.utc)
            created = user.created_at
            diff = current_time - created
            sec = diff.total_seconds()
            user_age = sec / 3600

            tweetfreq = user.statuses_count / user_age
            dataf['tweet_freq'].append(tweetfreq)
            
            followergrowth = user.followers_count / user_age
            dataf['followers_growth_rate'].append(followergrowth)
            
            friendsgrowth = user.friends_count / user_age
            dataf['friends_growth_rate'].append(friendsgrowth)
            
            favsgrowth = user.favourites_count / user_age
            dataf['favourites_growth_rate'].append(favsgrowth)
            
            listedgrowth = user.listed_count / user_age
            dataf['listed_growth_rate'].append(listedgrowth)
            
            if user.friends_count != 0:
                followfriend = user.followers_count / user.friends_count
                dataf['followers_friend_ratio'].append(followfriend)
            else:
                dataf['followers_friend_ratio'].append(-1)
            
            dataf['screenname_length'].append(len(screenname))
            dataf['name_length'].append(len(name))
            screen_name_digits = sum(c.isdigit() for c in screenname)
            name_digits = sum(c.isdigit() for c in name)
            dataf['num_digits_in_screenname'].append(screen_name_digits)
            dataf['name_digits_in_name'].append(name_digits)
            dataf['description_length'].append(len(user.description))
            if row[1] == "human" or row[1] == "genuine accounts":
                dataf['isbot'].append(0)
                
            else:
                dataf['isbot'].append(1)
            
        partial_dataframe = pd.DataFrame(data=dataf)
        #adds the information of the current user to the csv file
        partial_dataframe.to_csv('dataframee2.csv', mode='a', header=False)
        
            

    

def main():
    teach_easy_model()


if __name__ == "__main__":
    main()
