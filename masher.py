import json
from twitter import Twitter, OAuth
import tweepy
import random
from time import sleep
from google.cloud import translate
import pickle

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# This is the only way I know how to send tweets
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
tapi = tweepy.API(auth)

# This is the only way I know of to find tweets under a hashtags
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)

translate_client = translate.Client()

languages = ["af", "sq", "ar", "be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
            "vi", "cy", "yi"]


def itg(text, iter=5):
        for x in range(iter):
            text = translate_client.translate(text, target_language=random.choice(languages))[u'translatedText']
        text = translate_client.translate(text, target_language="en")[u'translatedText']
        return text

ids = pickle.load(open("twitter.ids", "rb"))

while True:
    tweets = twitter.search.tweets(q='#hackcu', count=100)
    pytweets = json.dumps(tweets)
    jtweets = json.loads(pytweets)
    real_tweets = jtweets['statuses']


    try:
        for tweet in real_tweets:
            if not(tweet['id'] in ids) and not(tweet['user']['screen_name']=="mlghackerbot"):

                garbage = itg(tweet['text'])
                tweet_text = "@"+tweet['user']['screen_name']+" "+garbage
                print tweet_text
                tapi.update_status(tweet_text, in_reply_to_status_id=tweet['id'])

                ids.append(tweet['id'])
                pickle.dump(ids, open("twitter.ids", "wb"))
    except:
        print "Ooops"

    print "on a break"
    sleep(30)
