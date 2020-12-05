#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:11:53 2020

@author: travismorenz
"""

import pandas as pd
import seaborn as sns
import sys

subreddit_names = [
    'askreddit',
    'videos',
    'funny',
    'news',
    'memes',
    'fantasy'
    ]

def plot_avgs(data, hue, title):
    g = sns.FacetGrid(data=data, col='day', hue=hue, col_order=days, col_wrap=4, sharex=False)
    g.fig.suptitle(title, y=1.03)
    g.map(sns.lineplot, "hour", "mean")
    g.set_axis_labels("Hour", "Avg Score")
    g.axes[0].legend()

original_stdout = sys.stdout

with open('output.txt', 'w') as output:
    # Set std out to file
    sys.stdout = output
    
    # Data frames
    df = pd.read_csv('dataset.csv')
    o = df[df['dataset'] == 'outliers'] # With outliers
    no = df[df['dataset'] == 'no outliers'] # Without outliers
    
    
    ###################################################################################################
    # Analyze best posting times
    ###################################################################################################
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Plot general avgs (with/without outliers)
    data =  df.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).reset_index()
    plot_avgs(data, 'dataset', 'General Findings')
    
    # Plot avgs by subreddit (with outliers)
    data = o.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
        .agg(['mean']).reset_index()
    plot_avgs(data, 'subreddit', 'By subreddit (with outliers)')
    
    # Plot avgs by subreddit (without outliers)
    data = no.groupby(['dataset', 'day', 'hour', 'subreddit'])['score']\
        .agg(['mean']).reset_index()
    plot_avgs(data, 'subreddit', 'By subreddit (without outliers)')
    
    # Get general best times
    print('General')
    top = o.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
    top_no = no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
    print(top)
    print(top_no)
    print()
    
    # Get best times for each subreddit
    for subreddit in subreddit_names:
        print('r/' + subreddit)
        sub = o[o['subreddit'] == subreddit]
        sub_no = no[no['subreddit'] == subreddit]
        top = sub.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
        top_no = sub_no.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).nlargest(3, 'mean')
        print(top)
        print(top_no)
        print()
    
    # Reset stdout
    sys.stdout = original_stdout