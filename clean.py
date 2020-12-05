#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:55:32 2020

@author: travismorenz
"""

from scipy import stats
import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data_v4.csv')
df2 = pd.read_csv('scraped_data_v0.csv')
df = df.append(df2, ignore_index=True)

df.to_csv('scraped_data_v5.csv', index=False)

df = df[(df['text'] != '[removed]') & (df['text'] != '[deleted]')]

zscores = np.abs(stats.zscore(df['score']))
df_no_outliers = df[zscores < 3]

df.to_csv('dataset.csv', index=False)
df_no_outliers.to_csv('dataset_no_outliers.csv', index=False)