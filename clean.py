#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:55:32 2020

@author: travismorenz
"""
import pandas as pd
import numpy as np
from scipy import stats
from textblob import TextBlob


def get_polarity(text):
    if type(text) != str:
        return np.nan
    polarity = TextBlob(text).sentiment.polarity
    return polarity


def get_sentiment(polarity):
    if np.isnan(polarity):
        return np.nan
    if polarity > 0.33:
        return 'positive'
    if polarity < -0.33:
        return 'negative'
    return 'neutral'


df = pd.read_csv('scraped_data_v5.csv')

# Filter out any posts that were removed or deleted
print('Filtering out nonexistant posts')
df = df[(df['text'] != '[removed]') & (df['text'] != '[deleted]')]

# Calculate post sentiments
print('Calculating sentiments')
df['title_polarity'] = df['title'].apply(get_polarity)
df['text_polarity'] = df['text'].apply(get_polarity)
df['title_sentiment'] = df['title_polarity'].apply(get_sentiment)
df['text_sentiment'] = df['text_polarity'].apply(get_sentiment)

# Create a separate dataframe without outliers
print('Removing outliers')
zscores = np.abs(stats.zscore(df['score']))
df_no = df[zscores < 3]

# Combine the two dataframes, making their items distinct (this is for visualization)
df['dataset'] = 'outliers'
df_no['dataset'] = 'no outliers'
df = df.append(df_no, ignore_index=True)

# Save to file
print('Saving')
df.to_csv('dataset.csv', index=False)