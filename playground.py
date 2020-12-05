#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:11:53 2020

@author: travismorenz
"""

import pandas as pd

df = pd.read_csv('reddit-data.csv')

datetimes = pd.to_datetime(df['created_at'], unit='s')
df['hours'] = datetimes.dt.hour

print(df['hours'])
print(df.loc[1])