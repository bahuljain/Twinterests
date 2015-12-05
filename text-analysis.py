import urllib2
import urllib
import json
import sys
import tweepy
import pickle

# biggest issue till now is implementing sessions. Need to restart server for each login

class Prismatic:
    def __init__(self, API_TOKEN):
        self.API_TOKEN = API_TOKEN

    def getTextTopic(self, text):
        prismUrl = 'http://interest-graph.getprismatic.com/text/topic'

        # The UrlRequestBody contains the URL of the website that needs to be analyzed
        # by Prismatic API. Note: It has to be in JSON format
        RequestBody = {
            'body' : text
        }

        data = urllib.urlencode(RequestBody)

        # create the request object and set some headers
        req = urllib2.Request(prismUrl, data)
        req.add_header('X-API-TOKEN', self.API_TOKEN)

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
    def getRelatedTopics(self, topicID):
        prismUrl = 'http://interest-graph.getprismatic.com/topic/topic?id=' + `topicID` + '&api-token=' + self.API_TOKEN
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
        self.prism = Prismatic(self.API_TOKEN)
        
    def loadTopicsDict(self):
        path = 'enriched-topics.pickle' if self.enriched else 'topics.pickle'
        with open(path, 'rb') as handle:
            topicsDict = pickle.load(handle)
        return topicsDict

    def generateNewInterests(self, last_tweet_id):
        # given the last_tweet_id find the total new tweets not analyzed and
        # check for last_tweet_id = -1 (which might not be needed in all)
        # check if volume of new tweets is significantly large only then do the following steps
        # analyze the tweets 
        # add to topics 

        # if last_tweet_id is -1:
        #     print "Sorry"
        success = False
        access_token = "563806852-9m6OTWv0bnpDfbEVYZXke1MoWwiB77IGRSpqwlaq"
        access_token_secret = "BsKrwRvSutkADZX73J53i2dTz3WgCPzSYj1KQ5NI5GQW5"
        consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
        consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        user = api.get_user(self.handle)
        total_tweets = user.statuses_count
        # pages_count = total_tweets / 10 if total_tweets % 10 is 0 else total_tweets / 10 + 1
        
        n = 1
        for page in tweepy.Cursor(api.user_timeline, self.handle, count=50).pages(5):
            tweets = ''
            print 'Page: ' + `n`
            offset = 1
            for status in page:
                count = (n-1)*50 + offset
                
                if status.id == last_tweet_id:
                    print "Tweets Extracted and Analyzed: " + `count`
                    return success
                else:
                    tweets += `status.text.lower().encode('ascii','ignore').decode('ascii')` + "\n"
                
                offset += 1
            n += 1

            success = True
            topics = self.prism.getTextTopic(tweets)

            print topics
            
            if topics:
                self.addTopics(topics)

        print "Tweets Extracted and Analyzed: " + `count`
        return success       


    def getTweets(self):
        #Variables that contains the user credentials to access Twitter API
        access_token = "563806852-9m6OTWv0bnpDfbEVYZXke1MoWwiB77IGRSpqwlaq"
        access_token_secret = "BsKrwRvSutkADZX73J53i2dTz3WgCPzSYj1KQ5NI5GQW5"
        consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
        consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"

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

            topics = self.prism.getTextTopic(tweets)
            if topics:
                self.addTopics(topics)

        print "Tweets Extracted and Analyzed: " + `count`
        # with open('topics.pickle', 'wb') as handle:
        #     pickle.dump(self.topicsDict, handle)
        # print "Pickle created"


    def addTopics(self, prism_result):
        for topic in prism_result["topics"]:
            if topic["id"] not in self.topicsDict:
                self.topicsDict[str(topic["id"])] = str(topic["topic"])

    def displayInterestTopics(self):
        for id in self.topicsDict:
            print `id` + ": " + self.topicsDict[id]

    def enrichTopicList(self):
        if len(self.topicsDict) is 0:
            print 'At least 1 topic should exist in Interests to enrich the Interests list.'
        while len(self.topicsDict) < 6:
            newTopicsList = []
            [newTopicsList.append(self.prism.getRelatedTopics(int(topic_id))) for topic_id in self.topicsDict]

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
user = User(handle, True)
last_tweet_id = 670091122098745345L # 672933917389922305L # 671947021331406848L
print last_tweet_id
print user.generateNewInterests(last_tweet_id)
# user.displayInterestTopics()
# user.getTweets()
# user.enrichTopicList()
# user.displayInterestTopics()
