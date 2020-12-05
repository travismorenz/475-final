#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:11:53 2020

@author: travismorenz
"""

import pandas as pd
import seaborn as sns


def get_best_posting_time():
    pass


df = pd.read_csv('dataset.csv')


### Conduct the analysis ###

# Analyze best posting times
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot avgs
group1 = df.groupby(['dataset', 'day', 'hour'])['score'].agg(['mean']).reset_index()
g = sns.FacetGrid(data=group1, col='day', hue='dataset', col_order=days, col_wrap=4, sharex=False)
g.map(sns.lineplot, "hour", "mean")
g.set_axis_labels("Hour", "Avg Score")
g.axes[0].legend()

# Get best in general

# Get best per subreddit
