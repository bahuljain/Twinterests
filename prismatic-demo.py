import urllib2
import urllib
import json
import sys

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
        print 'Prismatic: ' + `err.code` + ' - ' + err.reason
        return None

# takes a topic in the form of its ID and returns topics that are related to it.
def getRelatedTopics(API_TOKEN, topicID):
    prismUrl = 'http://interest-graph.getprismatic.com/topic/topic?id=' + `topicID` + '&api-token=' + API_TOKEN
    req = urllib2.Request(prismUrl)

    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError, err:
        print 'Prismatic: ' + `err.code` + ' - ' + err.reason
        return None


API_TOKEN = 'MTQ0NjM0MDg3NjkwNw.cHJvZA.YmtqMjExMUBjb2x1bWJpYS5lZHU.N4IRZXySkKJuJQ8G63RGlwZCyAU'
url = 'https://en.wikipedia.org/wiki/Machine_learning'

#print getUrlTopic(API_TOKEN, url3)
print getRelatedTopics(API_TOKEN, 25340)
