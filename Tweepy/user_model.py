import tweepy

#Variables that contains the user credentials to access Twitter API
access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('prakharsriv9')

# prakharsriv9

print user.screen_name + '\n'
print user.followers_count
print ''
for friend in user.friends():
   print friend.screen_name + '\n'
