import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
from tweepy import OAuthHandler
from decouple import config

#* Set Connecion

API_KEY = config('API_KEY')
API_KEY_SECRET = config('API_KEY_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
client = tweepy.Client(bearer_token = BEARER_TOKEN)

#* Create query

# Get tweets that contain the hashtag #monday
# -is:retweet means no retweets
# lang:en is asking for the english tweets
# Link to nice tutorial for queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
# Context_annotations: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
query = 'monday -is:retweet lang:en'
tweets = client.search_recent_tweets(query=query, max_results=10)


for count, tweet in enumerate(tweets.data):
    print(count + 1)
    print(tweet.text, end="\n\n")

