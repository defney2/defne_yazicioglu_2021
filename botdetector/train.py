import tweepy
import pickle
from datetime import datetime, timezone
#loads the finalized model to use on a given user and make a prediction

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))



consumer_key = "783ZxxFfcUkh4y5eG88JtgVG0"
consumer_secret = "10JlCd50Hpw0yICiTsHnYgNfcdiQGKxtDMM8ZRnpNsASPVHmug"
access_token = "921665261853466624-sYD4ZDpFA8CNHyeeKKwL2ZA1wwLrBtp"
access_token_secret = "TFRNyf6zlsvkKGi1j91bPdPr9LpRZ42Ta0TG7SLXlPmrm"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

val = input("Enter the twitter account screenname: ")


#use the tweepy module to get the user information and then input the user information to the trained model
user = api.get_user(screen_name=val)
screenname = user.screen_name
name = user.name

statuses_count = user.statuses_count
followers_count = user.followers_count
friends_count = user.friends_count
favourites_count = user.favourites_count
listed_count = user.listed_count
default_profile = user.default_profile
if default_profile == True:
    default_profile = 1
else:
    default_profile = 0
profile_use_background_image = user.profile_use_background_image
if profile_use_background_image == True:
    profile_use_background_image = 1
else:
    profile_use_background_image = 0
verified = user.verified
if verified == True:
    verified = 1
else:
    verified = 0


current_time = datetime.now(timezone.utc)
created = user.created_at
naive = current_time.replace(tzinfo=None)
diff = current_time - created
sec = diff.total_seconds()
user_age = sec / 3600
    
tweet_freq = user.statuses_count / user_age
followers_growth_rate = user.followers_count / user_age
friends_growth_rate = user.friends_count / user_age
favourites_growth_rate = user.favourites_count / user_age
listed_growth_rate = user.listed_count / user_age
followers_friend_ratio = user.followers_count / user.friends_count
screenname_length = len(screenname)
num_digits_in_screenname = sum(c.isdigit() for c in screenname)
name_length = len(name)
name_digits_in_name = sum(c.isdigit() for c in name)
description_length = len(user.description)

array = [statuses_count, followers_count, friends_count, favourites_count, listed_count, default_profile, profile_use_background_image, verified, tweet_freq, followers_growth_rate, friends_growth_rate, favourites_growth_rate, listed_growth_rate, followers_friend_ratio, screenname_length, num_digits_in_screenname, name_length, name_digits_in_name, description_length ]

loaded_model.predict([[statuses_count, followers_count, friends_count, favourites_count, listed_count, default_profile, profile_use_background_image, verified, tweet_freq, followers_growth_rate, friends_growth_rate, favourites_growth_rate, listed_growth_rate, followers_friend_ratio, screenname_length, num_digits_in_screenname, name_length, name_digits_in_name, description_length ]])

rf_probs1 = loaded_model.predict_proba([[statuses_count, followers_count, friends_count, favourites_count, listed_count, default_profile, profile_use_background_image, verified, tweet_freq, followers_growth_rate, friends_growth_rate, favourites_growth_rate, listed_growth_rate, followers_friend_ratio, screenname_length, num_digits_in_screenname, name_length, name_digits_in_name, description_length ]])[:, 1]

rf_probs0 = loaded_model.predict_proba([[statuses_count, followers_count, friends_count, favourites_count, listed_count, default_profile, profile_use_background_image, verified, tweet_freq, followers_growth_rate, friends_growth_rate, favourites_growth_rate, listed_growth_rate, followers_friend_ratio, screenname_length, num_digits_in_screenname, name_length, name_digits_in_name, description_length ]])[:, 0]

print("Probability human: ", rf_probs0)
print("Probability bot: ", rf_probs1)
