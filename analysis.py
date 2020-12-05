#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:11:53 2020

@author: travismorenz
"""

import numpy as np
import pandas as pd
from scipy import stats
from textblob import TextBlob


def sentiment_analysis(text):
    if type(text) != str:
        return None
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.33:
        return 'positive'
    if polarity < -0.33:
        return 'negative'
    return 'neutral'


def remove_outliers(df):
    zscores = np.abs(stats.zscore(df['score']))
    return df[zscores < 3]


def analyze_score(group, group2, name):
    mean = group['score'].mean()
    mean2 = group2['score'].mean()
    mean2.plot()


df = pd.read_csv('reddit-data.csv')

# Calculate post sentiments
df['title_sentiment'] = df['title'].apply(sentiment_analysis)
df['text_sentiment'] = df['text'].apply(sentiment_analysis)

# Create a dataframe without outliers
df_no_outliers = remove_outliers(df)

### Conduct the analysis ###

# Day grouping
group1 = df.groupby(['day'])
group2 = df_no_outliers.groupby(['day'])
analyze_score(group1, group2, 'General Day Grouping')
