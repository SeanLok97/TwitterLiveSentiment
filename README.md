The repository contains the code to retrieve tweets live from Twitter, and process them to give a live, updating sentiment score graph.

![ezgif-5-b165503aff3d](https://user-images.githubusercontent.com/66477337/100153157-a4863700-2e9b-11eb-9c20-27051d863573.gif)

For this code to work as intended, Twitter credentials must be pasted into the TwitterCredentials.py file, for more information
see https://developer.twitter.com/en/docs/twitter-api/tweets/hide-replies/quick-start

The refresh rate on line 81 of TwitterAPI.py heavily affects the number of tweets analysed. If set too low,
the code will miss some of the tweets sent, though this mostly affects high traffic search terms such as Trump.

Dependencies:
Tweepy
TextBlob
Numpy
PyQtGraph
PyQt5
Regex
Time
Collections
