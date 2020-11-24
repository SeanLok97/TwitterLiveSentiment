import TwitterCredentials
import tweepy
import re
from textblob import TextBlob
import pyqtgraph as pg
from collections import deque
import numpy as np
import time



class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.latest_tweet = ""
        self.Counter = 0

    def on_status(self, status):
        if not status.truncated:
            tweet = status.text
        else:
            tweet = status.extended_tweet['full_text']

        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet).split())
        tweet = ' '.join(re.sub('RT', ' ', tweet).split())
        self.latest_tweet = tweet
        self.Counter += 1
        #print("tweets received: " + str(self.Counter))
        return True

    def on_error(self, status_code):
        print("Tweepy error code: " + str(status_code))
        return False

    def get_latest_tweet(self):
        return self.latest_tweet


class Analyser:
    def __init__(self, memory):
        self.Sentiment = deque(maxlen=memory)
        self.Countervec = deque(maxlen=memory)
        self.Counter = 0

    def analysis(self, tweet):
        tweetblob = TextBlob(tweet)

        # Remove comment and add indentation if you wish to remove any sentiment score that is 0
        # if tweetblob.sentiment.polarity != 0:
        self.Sentiment.append(tweetblob.sentiment.polarity)
        self.Countervec.append(self.Counter)
        self.Counter += 1
        #print("tweets analysed: " + str(self.Counter))
        #print(tweet)
        return list(self.Countervec), list(self.Sentiment), self.Counter

        # return list(self.Countervec), list(self.Sentiment), self.Counter



if __name__ == "__main__":
    consumer_key = TwitterCredentials.consumer_key
    consumer_secret = TwitterCredentials.consumer_secret
    access_key = TwitterCredentials.access_key
    access_secret = TwitterCredentials.access_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    memory = 100

    listener = StreamListener()
    plotter = Analyser(memory)
    stream = tweepy.Stream(api.auth, listener, tweet_mode='extended',lang='zh')
    check = ""
    pw = pg.plot()
    pw.setYRange(-1,1)
    pg.QtGui.QApplication.processEvents()

    refreshrate = 0.01 #Refresh rate of the graph per second - the lower the number is, the more tweets that could be
                       # missed due to plotting efficiency (only affects very common terms such as Trump)
    searchterms = ['trump']

    stream.filter(track=searchterms, is_async=True)
    oldtime = time.time()
    while True:
        latest_tweet = listener.get_latest_tweet()
        if latest_tweet != check:
            x,y,counter = plotter.analysis(latest_tweet)
            check = latest_tweet
            print(latest_tweet)


            if time.time() - oldtime >= refreshrate:
                pw.plot(x, y, clear=True, symbol='o', pen=None)
                pw.addItem(pg.InfiniteLine(pos=np.mean(y), angle=0))
                pg.QtGui.QApplication.processEvents()
                oldtime = time.time()