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
def plot_polarity(df, title, hue=None):
    ax = sns.scatterplot(df['title_polarity'], df['score'], hue=hue)
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
    df = df[df['score'] > 5]
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
# General visualizations
###################################################################################################

# Bin submissions by their scores and plot
df_o['binned_scores'] = pd.cut(df['score'], [0, 5, 10, 20, 50, 100, 1000, 10000, 500000])
bins = df_o.groupby('binned_scores')['score'].agg(['count']).reset_index()
bins.index = ['0-5', '5-10', '10-20', '20-50', '50-100', '100-1000', '1000-10000', '10000+']
ax = bins.plot.pie(y='count')
ax.set_ylabel("Upvotes")
ax.set_title("Figure 1: Submissions by upvotes")


###################################################################################################
# Analyze best posting times
###################################################################################################

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot general avgs (with/without outliers)
data =  df.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).reset_index()
plot_avgs(data, 'dataset', 'Figure 2: Post times')

# Plot avgs by subreddit (with outliers)
data = df_o.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
    .agg(['mean']).reset_index()
plot_avgs(data, 'subreddit', 'Figure 3: Post times by subreddit (with outliers)')

# Plot avgs by subreddit (without outliers)
data = df_no.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
    .agg(['mean']).reset_index()
plot_avgs(data, 'subreddit', 'Figure 4: Post times by subreddit (without outliers)')

# Get general best times
output('General')
top = df_o.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(10, 'mean')
top_no = df_no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(10, 'mean')
output(top)
output(top_no)
output()

# Get best times for each subreddit
for subreddit in subreddit_names:
    output('r/' + subreddit)
    sub = df_o[df_o['subreddit'] == subreddit]
    sub_no = df_no[df_no['subreddit'] == subreddit]
    top = sub.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(10, 'mean')
    top_no = sub_no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
    output(top)
    output(top_no)
    output()


###################################################################################################
# Analyze sentiment
###################################################################################################

# Plot general polarity, discounting perfect 0's
plot_polarity(df_no[df_no['title_polarity'] != 0], 'Figure 5: Submission polarity')
output_sentiment_stats(df_no, 'General Polarity')

# Plot polarity without neutral
df_no_pn = df_no[df_no['title_sentiment'] != "neutral"]
plot_polarity(df_no_pn, 'Figure 6: Polarity w/o neutrals', df_no_pn['title_sentiment'])

# Plot polarities of each subreddit
g = sns.FacetGrid(data=df_no_pn, col='subreddit', hue='title_sentiment', col_wrap=4, sharex=False)
g.fig.suptitle('Figure 9: Polarity by subreddit', y=1.03)
g.map(sns.scatterplot, "title_polarity", "score")
g.set_axis_labels("Title Polarity", "Upvotes")
g.axes[0].legend()
plt.show()
plt.clf()

# Output polarity stats for each subreddit
for subreddit in subreddit_names:
    output_sentiment_stats(df_no[df_no['subreddit'] == subreddit], f"r/{subreddit} polarity")
    
# Plot news polarity specifically
df_news = df_no_pn[df_no_pn['subreddit'] == 'news']
plot_polarity(df_news, 'Figure 10: r/news polarity', hue=df_news['title_sentiment'])

# Output everything
with open('output.txt', 'w') as file:
    file.write(outputText)