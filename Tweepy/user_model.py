import tweepy

#Variables that contains the user credentials to access Twitter API
access_token = "563806852-xs7GDNNd81deP804KDInQllfKNPeSDXsChJD20fn"
access_token_secret = "U145Ujwy8DW0nTQZPNVsR0EfhP6LNcYYBF734mim6c0a9"
consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

print auth.access_token_secret

# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# user = api.get_user('prakharsriv9')
#
# # prakharsriv9
#
# print user.screen_name + '\n'
# print user.followers_count
# print ''
# for friend in user.friends():
#    print friend.screen_name + '\n'
