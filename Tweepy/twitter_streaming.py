# -*- coding: utf-8 -*-
#Import the necessary methods from tweepy library

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from HTMLParser import HTMLParser
#from pymongo import Connection

#Variables that contains the user credentials to access Twitter API
access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"
#keywordList = ['movies','sports','music','finance','technology','fashion','science','travel','health','cricket','india']

def findCategory(text, keywordList):
    category = []
    for keyword in keywordList:
        if keyword in text:
            category.append(keyword)
    return category

#This is a basic listener that just stores received tweets to database.
class StdOutListener(StreamListener):

    def __init__(self):
        self.counter = 0
        self.limit = 10

    def on_data(self, data):
        if self.counter < self.limit:
            decoded = json.loads(HTMLParser().unescape(data))

            #con = Connection()
            text = decoded['text'].lower().encode('ascii','ignore').decode('ascii')
            self.counter += 1
            print 'Tweet Count# ' + `self.counter`
            print text + '\n'

            """
            if decoded.get('coordinates',None) is not None:

                id = decoded['id']
                time = decoded.get('created_at','')
                text = decoded['text'].lower().encode('ascii','ignore').decode('ascii')
                coordinates = decoded.get('coordinates','').get('coordinates','')
                    category = findCategory(text, keywordList)
                db = con.twitterDatabase_test
                tweetsCollection = db.tweetsCollection_test
                tweetsCollection.insert({'_id':id,'timestamp':time,'text':text,'coordinates':coordinates,'category':category})

                self.counter += 1
                print 'Tweet Count# ' + `self.counter`
            """
        else:
            twitterStream.disconnect()

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authentification and the connection to Twitter Streaming API
    #while True:
    #    try:
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    twitterStream.filter(track=['travel','adventure'])
    #twitterStream.filter(track=[])
        #except:
        #    continue
