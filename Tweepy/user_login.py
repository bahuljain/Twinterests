import tweepy

#Variables that contains the user credentials to access Twitter API
access_token = "563806852-TgZSJkG413GrZ2g0TzRsyGh7lUAluLmrsKTCnKNs"
access_token_secret = "hqwb3QFb82LKXR10RAAbfEg8HBUMBQMsY8roZ9KySyar5"
consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"
callback_url = 'twitter.com'
verifier = '9179458'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
"""
token = session.get('request_token')
session.delete('request_token')
auth.request_token = token

"""

try:
    redirect_url = auth.get_authorization_url()
    print redirect_url
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

try:
    auth.get_access_token(verifier)
    print 'success'
except tweepy.TweepError:
    print 'Error! Failed to get access token.'
