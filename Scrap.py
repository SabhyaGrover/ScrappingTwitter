
import json
import csv
import tweepy
import re
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
hashtag_phrase='india'
"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)

    #open the spreadsheet we will write to
    with open('metadata.csv' , 'w') as file:

        w = csv.writer(file)

        #write header row to spreadsheet
        columns = ['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count']
        w.writerow([column for column in columns])

        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', \
                                   lang="en", tweet_mode='extended').items(100):
            w.writerow([tweet.created_at, tweet.full_text.replace('\n','').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'].encode('utf-8') for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

if __name__ == '__main__':
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
