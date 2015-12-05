import urllib2
import urllib
import json
import sys
import tweepy

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
        # generating the request url containing parameters
        prismUrl = 'http://interest-graph.getprismatic.com/topic/topic?id=' + `topicID` + '&api-token=' + self.API_TOKEN
        
        # sending a request to prismatic
        req = urllib2.Request(prismUrl)

        # handling the response and errors if any
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

class UserInterests:
    def __init__(self, api, topics):
        if topics is None:
            self.topicsDict = dict()
        else: 
            self.topicsDict = topics
        self.API_TOKEN = 'MTQ0NjM0MDg3NjkwNw.cHJvZA.YmtqMjExMUBjb2x1bWJpYS5lZHU.N4IRZXySkKJuJQ8G63RGlwZCyAU'
        self.prism = Prismatic(self.API_TOKEN)
        self.api = api
        
    # def getNewTweetsCount():
    def generateNewInterests(self, last_tweet_id):
        success = False
        
        user = self.api.me()
        total_tweets = user.statuses_count
        
        n = 1
        for page in tweepy.Cursor(self.api.user_timeline, count=50).pages(5):
            tweets = ''
            print 'Page: ' + `n`
            offset = 1
            for status in page:
                count = (n-1)*10 + offset
                
                if status.id == last_tweet_id:
                    print "Tweets Extracted and Analyzed: " + `count`
                    return success
                else:
                    tweets += `status.text.lower().encode('ascii','ignore').decode('ascii')` + "\n"
                
                offset += 1
            n += 1
            
            success = True
            topics = self.prism.getTextTopic(tweets)
            
            if topics:
                self.addTopics(topics)

        print "Tweets Extracted and Analyzed: " + `count`
        return success

    def generateInterests(self):
        user = self.api.me()
        total_tweets = user.statuses_count
        page_size = 50 #if total_tweets < 1000 else 100
        page_count = 10 #if page_size is 50 else 10
        
        page_list = []
        n = 1
        for page in tweepy.Cursor(self.api.user_timeline, count=page_size).pages(page_count):
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

    # prism_result - the result from prismatic as it is
    def addTopics(self, prism_result):
        for topic in prism_result["topics"]:
            if str(topic["id"]) not in self.topicsDict:
                self.topicsDict[str(topic["id"])] = str(topic["topic"])

    def displayInterestTopics(self):
        for id in self.topicsDict:
            print `id` + ": " + self.topicsDict[id]

    def getInterests(self):
        return self.topicsDict

    def enrichTopicList(self):
        if len(self.topicsDict) is 0:
            print 'Need more tweets to get interests'
        else:
            count = 0
            while len(self.topicsDict) < 5 and count < 5:
                newTopicsList = []
                [newTopicsList.append(self.prism.getRelatedTopics(int(topic_id))) for topic_id in self.topicsDict]

                [self.addTopics(result) for result in newTopicsList]
                count += 1

# # Bahul - bahulkjain
# # Prakhar - prakharsriv9
# API_TOKEN = 'MTQ0NjM0MDg3NjkwNw.cHJvZA.YmtqMjExMUBjb2x1bWJpYS5lZHU.N4IRZXySkKJuJQ8G63RGlwZCyAU'
# prism = Prismatic(API_TOKEN)
# print prism.getRelatedTopics(2607)