#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 20:30:38 2020

@author: travismorenz
"""
from datetime import datetime, timedelta, timezone
import pandas as pd
import requests
import json
import praw
import time

# Auth for reddit API (idc about this being public, I don't use it)
auth = {
    'client_id': 'IkBRcae8H0nFhg',
    'client_secret': 'RtM7GOE_2OcK5sD8NpM-oj6uCpUpFw',
    'user_agent': '475 Project',
    'username': 'redditscraper4000',
    'password': 'Letmeinyo1',
    }

subreddit_names = [
    'askreddit',
    'videos',
    'funny',
    'news',
    'memes',
    'fantasy'
    ]

df = pd.DataFrame(columns=[
        'id',
        'subreddit',
        'title',
        'score',
        'upvote_ratio',
        'text',
        'created_at',
        ])


# Gets posts on a given subreddit between a range of times using the PushShift API
def pushshift_query(subreddit, after, before):
    url = f"https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={before}&after={after}&sort=desc&sort_type=score&size=500"
    try:
        r = requests.get(url)
        data = json.loads(r.text)
    except:
        return False
    return data['data']


totaltime = 0 # Track total scraping time

# Scrape posts from each subreddit at a time
for version, subreddit in enumerate(subreddit_names):
    starttime = time.time()
    
    # Make 730 calls to the PushShift API (one for each hour in a month)
    # Initially, I store only the ids of the posts because the rest of the metadata is not up to date
    ids = []
    print(f"***Collecting posts for {subreddit}***")
    for i in range(730):
        
        if i > 23 and i % 24 == 0:
            print(f"Day {int(i / 24)} complete")
            print(f"Total of {len(ids)} post ids collected")
            print()
    
        dt = datetime(2020, 11, 1)
        start_td = timedelta(hours = i)
        end_td = timedelta(hours = i+1)
        
        after = (dt + start_td).replace(tzinfo=timezone.utc).timestamp()
        before = (dt + end_td).replace(tzinfo=timezone.utc).timestamp()
        data = pushshift_query(subreddit, int(after), int(before))
        
        if not data:
            continue
        
        for submission in data:
            if submission['id'] not in ids:
                ids.append(submission['id'])
    
    
    # Now I query the reddit API directly to get the updated metadata for the posts I have and add them to the dataframe
    print("Populating dataframe")
    ids = [f"t3_{x}" for x in ids]
    reddit = praw.Reddit(**auth)
    for post in reddit.info(fullnames=ids):
        df = df.append({
                'id': post.id,
                'subreddit': subreddit,
                'title': post.title,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'text': post.selftext,
                'created_at': post.created_utc
                }, ignore_index=True)
        
        
    # Save the specific day of the week and hour the posts were made into new columns for easy access
    datetimes = pd.to_datetime(df['created_at'], unit='s')
    df['day'] = datetimes.dt.day_name()
    df['hour'] = datetimes.dt.hour
    
    # Save current version of the dataframe to file
    df.to_csv(f"scraped_data_v{version}.csv", index=False)
    
    elapsed = int(time.time() - starttime)
    totaltime += elapsed
    print(f"Finished after {elapsed} seconds")
    print("-----------------------------------------------------------")
    print()

print(f"Total time elapsed: {totaltime} seconds")