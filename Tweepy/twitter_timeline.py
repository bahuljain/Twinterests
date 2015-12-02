import tweepy

#Variables that contains the user credentials to access Twitter API
access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()

# Bahul - bahulkjain
# Prakhar - prakharsriv9

user_tweets = api.user_timeline(handle, count=100)
# limit = 10
limit = 1

f = open('tweets-' + handle + '.txt','w')
for tweet in user_tweets:
    # if limit > 0:
    text = tweet.text.lower().encode('ascii','ignore').decode('ascii')
    f.write(`limit` + ": " + `tweet` + "\n")
    print len(text)
    # print `limit` + ": " + tweet.text.lower().encode('ascii','ignore').decode('ascii')
    limit += 1
    # else:
    #     break
# .lower().encode('ascii','ignore').decode('ascii')


f.close()
