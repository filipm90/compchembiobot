# CompChemBioBot/config.py

'''

Configuration file aims to set the API connectection with Twitter account using a set of credentials defined in 'keys';
In case the credentials are changed, please update the 'keys'; 

'''

import tweepy
import logging

logger = logging.getLogger()

# Key credentials for CompChemBioBot account;
# When applying for credential keys, apply for 'Read, Write, and Direct Messages' permission;
# Change the values in 'keys' dictionary to use your credentials;

keys = {"api": "", #API key
        "api_secret": "", #API key secret
        "token": "", #Access token
        "token_secret": "" #Access token secret}

def create_api():

    auth = tweepy.OAuthHandler(keys["api"], keys["api_secret"])
    auth.set_access_token(keys["token"], keys["token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as ex:
        logger.error("Error creating API", exc_info=True)
        raise ex
    logger.info("API created")
    return api