import urllib2
import urllib
import json
import sys
import tweepy
import pickle

def getTextTopic(API_TOKEN, text):
    prismUrl = 'http://interest-graph.getprismatic.com/text/topic'

    # The UrlRequestBody contains the URL of the website that needs to be analyzed
    # by Prismatic API. Note: It has to be in JSON format
    RequestBody = {
        'body' : text
    }

    data = urllib.urlencode(RequestBody)

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

class User:
    def __init__(self, handle, enriched):
        self.enriched = enriched
        self.topicsDict = self.loadTopicsDict()
        self.handle = handle
        self.API_TOKEN = 'MTQ0NjM0MDg3NjkwNw.cHJvZA.YmtqMjExMUBjb2x1bWJpYS5lZHU.N4IRZXySkKJuJQ8G63RGlwZCyAU'

    def loadTopicsDict(self):
        path = 'enriched-topics.pickle' if self.enriched else 'topics.pickle'

        with open(path, 'rb') as handle:
            topicsDict = pickle.load(handle)
        return topicsDict

    def getTweets(self):
        #Variables that contains the user credentials to access Twitter API
        access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
        access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
        consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
        consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        page_list = []
        n = 1
        for page in tweepy.Cursor(api.user_timeline, self.handle, count=100).pages(5):
            print 'Page: ' + `n`
            page_list.append(page)
            n = n+1

        count = 1

        for page in page_list:
            tweets = ''
            for status in page:
                count += 1
                tweets += `status.text.lower().encode('ascii','ignore').decode('ascii')` + "\n"

            topics = getTextTopic(self.API_TOKEN, tweets)
            if topics:
                self.addTopics(topics)

        print "Tweets Extracted and Analyzed: " + `count`
        # with open('topics.pickle', 'wb') as handle:
        #     pickle.dump(self.topicsDict, handle)
        # print "Pickle created"


    def addTopics(self, prism_result):
        for topic in prism_result["topics"]:
            if topic["id"] not in self.topicsDict:
                self.topicsDict[topic["id"]] = topic["topic"]

    def displayInterestTopics(self):
        for id in self.topicsDict:
            print `id` + ": " + self.topicsDict[id]

    def enrichTopicList(self):
        newTopicsList = []
        [newTopicsList.append(getRelatedTopics(self.API_TOKEN, id)) for id in self.topicsDict]

        [self.addTopics(result) for result in newTopicsList]

        print ''
        self.displayInterestTopics()
        print ''
        #
        # with open('enriched-topics.pickle', 'wb') as handle:
        #     pickle.dump(self.topicsDict, handle)
        # print "Pickle created"

# Bahul - bahulkjain
# Prakhar - prakharsriv9
handle = 'prakharsriv9'
# tweets = getTweets(handle)
user = User(handle, False)
# user.getTweets()
# user.enrichTopicList()
user.displayInterestTopics()
