import pandas as pd
import tweepy
import re
from decouple import config
from textblob import TextBlob

#* Set Connecion
API_KEY = config('API_KEY')
API_KEY_SECRET = config('API_KEY_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
client = tweepy.Client(bearer_token = BEARER_TOKEN)


#* Fetch and Print Tweets
# Get tweets that contain the word monday
# -is:retweet means no retweets
# lang:en is asking for the english tweets
# Link to nice tutorial for queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
# Context_annotations: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
query = 'arsenal -is:retweet lang:en'
tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at'], max_results=10)

# for count, tweet in enumerate(tweets.data):
#     print("TWEET ", count)
#     print("Created at: ", tweet.created_at, end="\n\n")
#     print(tweet.text, end="\n\n")
#     print("------------------------------------------------------------------------", end="\n\n")


#* Create dataframe
df = pd.DataFrame(tweets.data)
df = df.drop(['id'], axis=1)


#* Clean Data
def clean_tweet(tweet):
    """
    (@[A-Za-z0-9]+)   : Delete Anything like @hello @Letsupgrade etc
    ([^0-9A-Za-z \t]) : Delete everything other than text,number,space,tabspace
    (\w+:\/\/\S+)     : Delete https://
    ([RT]) : Remove "RT" from the tweet
    
    """
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])', ' ', str(tweet).lower()).split())

df['clean_text'] = df['text'].apply(lambda x : clean_tweet(x))


#* Analyze Sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df["sentiment"] = df["clean_text"].apply(lambda x : analyze_sentiment(x))

for index in df.index:
    print(index, df['sentiment'][index], df['clean_text'][index], sep=" | ", end="\n\n")