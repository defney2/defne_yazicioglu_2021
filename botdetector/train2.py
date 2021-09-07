import pandas as pd
import numpy as np
import seaborn as sns
import tweepy
from datetime import datetime, timezone
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import model_selection
import pickle

#this is the python script that builds a model that fits the dataset using the random forest model.

columns = ['statuses_count', 'followers_count', 'friends_count',
'favourites_count', 'listed_count', 'default_profile',
'profile_use_background_image', 'verified', 'tweet_freq',
'followers_growth_rate', 'friends_growth_rate',
'favourites_growth_rate', 'listed_growth_rate',
'followers_friend_ratio', 'screenname_length',
'num_digits_in_screenname', 'name_length', 'name_digits_in_name',
'description_length', 'isbot']

dataset = pd.read_csv("scraped_tweets.csv", usecols = columns)

def binary_map(x):
    return x.map({True: 1, False: 0})

altered_var = ['default_profile',
'profile_use_background_image',
'verified']

dataset[altered_var] = dataset[altered_var].apply(binary_map)
dataset.head()
dataset.columns
dataset.shape
dataset.describe()
dataset.isnull().sum()
#create new dataset where the null values are dropped and check that there are no null values left
dataset1 = dataset.dropna()
dataset1.isnull().sum()

train = dataset1.drop(['isbot'], axis = 1)
test = dataset1['isbot']

X_train, X_test, y_train, y_test = train_test_split(train, test, train_size = 0.8, test_size = 0.2, random_state = 2)
regr = LinearRegression()
regr.fit(X_train, y_train)



pred = regr.predict(X_test)

#since linear regression gave a very low accuracy score I moved onto try a different model: the random forest model
regr.score(X_test, y_test)

clf=RandomForestClassifier(n_estimators=100)
clf.fit(X_train,y_train)

#saved the finalized model to later be loaded 
filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))


y_pred=clf.predict(X_test)



metrics.accuracy_score(y_test, y_pred)



