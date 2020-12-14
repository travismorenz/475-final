#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:11:53 2020

@author: travismorenz
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


subreddit_names = [
    'askreddit',
    'videos',
    'funny',
    'news',
    'memes',
    'fantasy'
    ]

outputText = ""

# For creating the time plots
def plot_avgs(data, hue, title):
    g = sns.FacetGrid(data=data, col='day', hue=hue, col_order=days, col_wrap=4, sharex=False)
    g.fig.suptitle(title, y=1.03)
    g.map(sns.lineplot, "hour", "mean")
    g.set_axis_labels("Hour", "Avg Score")
    g.axes[0].legend()
    plt.show()
    plt.clf()
    
    
# For creating the polarity plots
def plot_polarity(df, title):
    ax = sns.scatterplot(df['title_polarity'], df['score'])
    ax.set_ylabel("Score")
    ax.set_xlabel("Title Polarity")
    ax.set_title(title)
    plt.show()
    plt.clf()
    
    
def output_sentiment_stats(df, title):
    output(title)
    stats = df.groupby(['title_sentiment'])["score"].agg(['mean', 'count'])
    output(stats)
    output('Filter on low scores')
    df = df[df['score'] > 100]
    stats = df.groupby(['title_sentiment'])["score"].agg(['mean', 'count'])
    output(stats)
    output()
    

# Acts as a print fn, except that it pipes to a file
def output(txt=''):
    global outputText
    outputText = outputText + "\n" + str(txt)

# Data frames
df = pd.read_csv('dataset.csv')
df_o = df[df['dataset'] == 'outliers'] # With outliers
df_no = df[df['dataset'] == 'no outliers'] # Without outliers


###################################################################################################
# Analyze best posting times
###################################################################################################

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot general avgs (with/without outliers)
data =  df.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).reset_index()
plot_avgs(data, 'dataset', 'General Findings')

# Plot avgs by subreddit (with outliers)
data = df_o.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
    .agg(['mean']).reset_index()
plot_avgs(data, 'subreddit', 'By subreddit (with outliers)')

# Plot avgs by subreddit (without outliers)
data = df_no.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
    .agg(['mean']).reset_index()
plot_avgs(data, 'subreddit', 'By subreddit (without outliers)')

# Get general best times
output('General')
top = df_o.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
top_no = df_no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
output(top)
output(top_no)
output()

# Get best times for each subreddit
for subreddit in subreddit_names:
    output('r/' + subreddit)
    sub = df_o[df_o['subreddit'] == subreddit]
    sub_no = df_no[df_no['subreddit'] == subreddit]
    top = sub.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
    top_no = sub_no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
    output(top)
    output(top_no)
    output()


###################################################################################################
# Analyze sentiment
###################################################################################################

# Plot general polarity
plot_polarity(df_no, 'General Polarity')
output_sentiment_stats(df_no, 'General Polarity')

# Plot polarity without neutral
df_no_pn = df_no[df_no['title_sentiment'] != "neutral"]
plot_polarity(df_no_pn, 'Polarity w/o neutrals')

# TODO: Do for all subreddits
# Plot news polarity
df_no_news = df_no[df_no['subreddit'] == "news"]
plot_polarity(df_no_news, 'News Polarity')
output_sentiment_stats(df_no_news, 'News Polarity')

df_no_news_pn = df_no_pn[df_no_pn['subreddit'] == "news"]
plot_polarity(df_no_news_pn, 'News polarity w/o neutrals')




# Output everything
with open('output.txt', 'w') as file:
    file.write(outputText)