import urllib2
import urllib
import json
import sys
import tweepy

def getTweets(handle):
    #Variables that contains the user credentials to access Twitter API
    access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
    access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
    consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
    consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()

    # Bahul - bahulkjain
    # Prakhar - prakharsriv9
    user_tweets = api.user_timeline(handle, count=100)
    limit = 1

    tweets = ''
    for tweet in user_tweets:
        text = tweet.text.lower().encode('ascii','ignore').decode('ascii')
        tweets += text
        limit += 1
    return tweets

# takes a url (not encoded format) and tags it with topics
def getUrlTopic(API_TOKEN, url):
    prismUrl = 'http://interest-graph.getprismatic.com/url/topic'

    # The UrlRequestBody contains the URL of the website that needs to be analyzed
    # by Prismatic API. Note: It has to be in JSON format
    UrlRequestBody = {
        'url' : url
    }

    data = urllib.urlencode(UrlRequestBody)

    # create the request object and set some headers
    req = urllib2.Request(prismUrl, data)
    req.add_header('X-API-TOKEN', API_TOKEN)

    # make the request and return the results
    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError, err:
        display = 'Prismatic: ' + `err.code` + ' - '
        if err.code == 400:
            print display + 'Not enough extracted text to run analysis'
        else:
            print display + err.reason
        return None

# takes a topic in the form of its ID and returns topics that are related to it.
def getRelatedTopics(API_TOKEN, topicID):
    prismUrl = 'http://interest-graph.getprismatic.com/topic/topic?id=' + `topicID` + '&api-token=' + API_TOKEN
    req = urllib2.Request(prismUrl)

    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError, err:
        display = 'Prismatic: ' + `err.code` + ' - '
        if err.code == 400:
            print display + 'Not enough extracted text to run analysis'
        else:
            print display + err.reason
        return None

def getTextTopic(API_TOKEN, text):
    prismUrl = 'http://interest-graph.getprismatic.com/text/topic'

    # The UrlRequestBody contains the URL of the website that needs to be analyzed
    # by Prismatic API. Note: It has to be in JSON format
    RequestBody = {
        'body' : text
    }

    data = urllib.urlencode(UrlRequestBody)

    # create the request object and set some headers
    req = urllib2.Request(prismUrl, data)
    req.add_header('X-API-TOKEN', API_TOKEN)

    # make the request and return the results
    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError, err:
        display = 'Prismatic: ' + `err.code` + ' - '
        if err.code == 400:
            print display + 'Not enough extracted text to run analysis'
        else:
            print display + err.reason
        return None

API_TOKEN = 'MTQ0NjM0MDg3NjkwNw.cHJvZA.YmtqMjExMUBjb2x1bWJpYS5lZHU.N4IRZXySkKJuJQ8G63RGlwZCyAU'
handle = 'prakharsriv9'
tweets = getTweets(handle)

print getTextTopic(API_TOKEN, tweets)
#
#
# url = 'https://en.wikipedia.org/wiki/M  achine_learning'
# url2 = 'https://analytics.twitter.com/research/surveys/1089?cs=47a8f7'
#
# print getUrlTopic(API_TOKEN, "srgsrg")







# print getRelatedTopics(API_TOKEN, 25340)
