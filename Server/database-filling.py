import tweepy
from dynamo import DynamoTable
from interests import UserInterests

class Filler:

	def home(self,handle):
		access_token = "563806852-9m6OTWv0bnpDfbEVYZXke1MoWwiB77IGRSpqwlaq"
		access_token_secret = "BsKrwRvSutkADZX73J53i2dTz3WgCPzSYj1KQ5NI5GQW5"
		consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
		consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)
		user = api.get_user(handle)

		print user.name + " has logged in"

		dynamo = DynamoTable('default', 'twitty-users')
    
		if dynamo.checkUserExists(user.id) is False:
			print "New User"

			interests = UserInterests(api, None)

			interests.generateInterests(handle)
			interests_dict = interests.getInterests()
			print interests_dict

			# print "\nEnriching Interests"
			# interests.enrichTopicList()
			# interests_dict = interests.getInterests()
			# print interests_dict

			print "interests generated"

			last_tweet_id = user.status.id if len(interests_dict) is not 0 else -1L
			print "Last Tweet ID: " + `last_tweet_id`

			User = {
				'user_id': user.id,
				'name': user.name,
				'screen_name': user.screen_name,
				'profile_image_url': user.profile_image_url,
				'location': user.location if len(user.location) > 0 else 'Earth, Milky Way',
				'follower_count': user.followers_count,
				'friends_count': user.friends_count,
				'profile_url': "http:/twitter.com/" + user.screen_name,
				'description': user.description if len(user.description) > 0 else 'Sorry I have no description',
				'statuses_count': user.statuses_count,
				'interests': interests_dict,
				'interests_count': len(interests_dict),
				'last_tweet_id': last_tweet_id
			}

			print "User Item created"

			dynamo.addUserToDB(User)
			print "User added to DB"
		
		else:
			print "User already exists"

filler = Filler()

users = [
	'andersoncooper'
]

for i in range(0,3):
	filler.home(users[i])