from collections import Counter

import matplotlib.pyplot as plt
import tweepy
from nltk import word_tokenize, re
from prettytable import PrettyTable
from textblob import TextBlob
import datetime as dt
import twitterscraper
from twitterscraper import query_tweets_from_user
from twitterscraper import query_tweets


def clean_text(tweet):
    '''
    Regular expression that removes links and special characters from tweet.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    '''
    Calculate the sentiment using TextBlob module
    TextBlog
    '''
    text = clean_text(tweet)
    print(text)
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_tweets_sentiment(query, limit=10):
    '''
    Given a query returns the tweets
    '''
    tweets = []
    start = dt.date(2019, 5, 30)
    end = dt.date(2019, 5, 31)
    lang = 'english'

    try:
        # calls the API to obtain tweets
        fetched_tweets = query_tweets(query, limit=limit, begindate=start,
                                      enddate=end, lang=lang)

        # parsing the tweets
        for tweet in fetched_tweets:
            parsed_tweet = {}
            # get the tweet text
            parsed_tweet['text'] = tweet.text
            # get the sentiment for the tweet's text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
            # add the tweet to our list and avoid retweets
            if tweet.retweets > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets
    except Exception as e:
        print("Error : %s" % str(e))


def sentiment_analysis_example(query="blockchain", count=100):
    tweets = get_tweets_sentiment(query, limit=count)
    print(tweets)
    print(len(tweets))
    ptweets = [tweet for tweet in tweets
               if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets
               if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # print the first five positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:5]:
        print(tweet['text'])
    # print the first five negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:5]:
        print(tweet['text'])


def get_tweets(query, count=10):
    '''
    Restituisce i tweet data una query particolare
    '''
    tweets = []
    try:
        # calls the API to obtain tweets
        fetched_tweets = query_tweets(query, limit=count)
        # parsing the tweets
        for tweet in fetched_tweets:
            # add the tweet to our list and avoid retweets
            if tweet.retweet_count > 0:
                if tweet.text not in tweets:
                    tweets.append(tweet.text)
            else:
                tweets.append(tweet.text)
        return tweets
    except Exception as e:
        print("Error : %s" % str(e))


if __name__ == '__main__':
    query = "donald trump"
    count = 10
    sentiment_analysis_example(query, count)
