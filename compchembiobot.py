#!/usr/bin/python3
# CompChemBioBot/compchembiobot.py

import tweepy
import logging
from config import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Keywords used for liking and retweeting
# Following 'keywords' should represent computational life sciences community and can be changed to follow the trends;

keywords = ['#compchem', '#compbio', #computational chemistry & biology
            '#chemoinformatics', '#cheminformatics', '#bioinformatics', '#molecularmodeling', #chemoinformatics & bioinformatics
            '#medchem', '#chembio', #medicinal chemistry & chemical biology
            '#drugdesign', '#drugdiscovery' #drug design (discovery)
            ]

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            return #Replies and own tweets will be ignored;
        if not hasattr(tweet, "retweeted_status"): #avoid retweets
            if tweet.is_quote_status == False: #avoid quoted tweets
                if not tweet.favorited:
                    try:
                        tweet.favorite() #like the tweet first;
                        logger.info(f' {tweet.id} liked!')
                    except Exception as ex:
                        logger.error("Error on fav", exc_info=True)
                if not tweet.retweeted:
                    try:
                        tweet.retweet() #and then retweet it;
                        logger.info(f' {tweet.id} retweeted!')
                    except Exception as ex:
                        logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        #This will stop the stream only for error 420 (exceeded number of attempts to reconnect)
        #For other errors it will reconnect the stream, with backoff
        if status == 420:
            return False
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"], is_async=True) #if the connection closes, the thread is blocked (is_async = True runs stream on a new thread and saves it)

if __name__ == "__main__":
    main(keywords)