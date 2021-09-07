import matplotlib
from sklearn.decomposition import PCA
from datetime import datetime
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
#from utils import display_pca_scatterplot
import json
import tensorflow as tf
import pandas as pd
import random
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics import f1_score, classification_report
from spacy.tokenizer import Tokenizer
from spacy.lang.tr import Turkish
import numpy as np
import warnings
from tqdm import tqdm
import matplotlib.pyplot as plt
import torch

#this python test script uses BERT to sentiment analyze turkish tweets in a csv file

def filter(text):
    final_text = ''
    for word in text.split():
        if word.startswith('@'):
            continue
        elif word[-3:] in ['com', 'org']:
            continue
        elif word.startswith('pic') or word.startswith('http') or word.startswith('www'):
            continue
        else:
            final_text += word+' '
    return final_text


# check GPU
device = 'cpu'


tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")
bert = AutoModel.from_pretrained("dbmdz/bert-base-turkish-128k-uncased").to(device)

def feature_extraction(text):
    x = tokenizer.encode(filter(text))
    with torch.no_grad():
        x, _ = bert(torch.stack([torch.tensor(x)]).to(device))
        return list(x[0][0].cpu().numpy())

        

def analyzer():
    with open("train.json", 'r') as f:
        train = json.load(f)

    with open("test.json", 'r') as f:
        test = json.load(f)


    mapping = {'negative':0, 'notr':1, 'positive':2}
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    for element in tqdm(train):
        X_train.append(feature_extraction(element['sentence']))
        y_train.append(mapping[element['value']])
    for element in tqdm(test):
        X_test.append(feature_extraction(element['sentence']))
        y_test.append(mapping[element['value']])
        

    model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=1000, activation='tanh', solver='adam', alpha=1e-5, learning_rate='constant',
                          verbose=1, early_stopping=True)
    model.fit(X_train, y_train)
    y_true, y_pred = y_test, model.predict(X_test)
    print(classification_report(y_true, y_pred))


    df = pd.read_csv("scraped_tweets.csv")
    df['value'] = 0
    
    neutralcount = 0
    positivecount = 0
    negativecount = 0
    for idx, row in df.iterrows():
        X = feature_extraction(row['text'])
        df.at[idx, 'value'] = model.predict([X])[0]-1
        if df.at[idx, 'value'] == 0:
            neutralcount = neutralcount + 1
        
        elif df.at[idx, 'value'] == 1:
            positivecount = positivecount + 1

        elif df.at[idx, 'value'] == -1:
            negativecount = negativecount + 1
     
    total = neutralcount + positivecount + negativecount
    print("Total Tweet Number = " + str(total))
    print("Positive Tweet Number = " + str(positivecount))
    print("Negative Tweet Number = " + str(negativecount))
    print("Neutral Tweet Number = " + str(neutralcount))
    
    df.to_csv('output.csv')
    
    
