#!/usr/bin/python3
# CompChemBioBot/compchembiobot.py

import json
import tweepy
import logging
import datetime
from config import create_api
from http.client import IncompleteRead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Keywords used for liking and retweeting
# Following 'keywords' should represent computational life sciences community and can be changed to follow the trends;

my_id = 1161989954819559424 #Twitter ID of my personal account

keywords = ['#compchem', '#compbio', #computational chemistry & biology
            '#chemoinformatics', '#cheminformatics', '#bioinformatics', '#molecularmodeling', #chemoinformatics & bioinformatics
            '#medchem', '#chembio', #medicinal chemistry & chemical biology
            '#drugdesign', '#drugdiscovery' #drug design (discovery)
            ]

skip_tweet = []

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.id not in skip_tweet:
            try:
                logger.info(f"Processing tweet id {tweet.id}")
                if tweet.in_reply_to_status_id is not None or \
                    tweet.user.id == self.me.id:
                    return #Replies and own tweets will be ignored;
                if not hasattr(tweet, "retweeted_status"):
                    if tweet.is_quote_status == False: #avoid retweeted and quoted tweets
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
            except IncompleteRead:
                skip_tweet.append(tweet.id)
                pass

    def on_error(self, status):
        #This will stop the stream only for error 420 (exceeded number of attempts to reconnect)
        #For other errors it will reconnect the stream, with backoff
        if status == 420:
            end_time = str(datetime.datetime.now() - start_time)
            direct_message = api.send_direct_message(my_id, f"I'm down, please let me work again. :( My end time is {end_time}")
            logger.error(direct_message.message_create['message_data']['text'])
            return False
        direct_message = api.send_direct_message(my_id, f"Oh, error {status} appeared. I hope everything is okay with me...")
        logger.error(direct_message.message_create['message_data']['text'])

def main(keywords):
    api = create_api()
    start_time = datetime.datetime.now()
    direct_message = api.send_direct_message(my_id, f"I'm alive and ready to work! :) My start time is {start_time}")
    logger.info(direct_message.message_create['message_data']['text'])
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"], is_async=True) #if the connection closes, the thread is blocked (is_async = True runs stream on a new thread and saves it)

if __name__ == "__main__":
    main(keywords)
