import boto3.session
from boto3.dynamodb.conditions import Key, Attr
import tweepy

class DynamoTable:

	def __init__(self, profileName, tableName):
		self.boto3 = boto3.session.Session(profile_name=profileName)
		self.dynamo = self.boto3.resource('dynamodb', 'us-east-1')
		self.table = self.dynamo.Table(tableName)

	# returns the entire table
	def scanTable(self):
		result = self.table.scan()
		print "Fetched: " + `result['Count']` + " Users" 
		return result["Items"]

	# adding a new entry in the database
	def addUserToDB(self, user, interests_dict, last_tweet_id):
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

		response = self.table.put_item(Item=User)
		print response

	# Self-Explanatory
	def checkUserExists(self, id):
		response = self.table.query(
	    	KeyConditionExpression=Key('user_id').eq(id)
		)
		return True if response['Count'] > 0 else False

	# Returns the user entry in the database given the user_id
	def getUser(self, user_id):
		result = self.table.query(
			KeyConditionExpression=Key('user_id').eq(user_id)
		)
		return result['Items'][0] if result['Count'] > 0 else None

	# updating the interests of user in the database
	def updateInterests(self, rowUserId, last_tweet_id, interests):
		response = self.table.update_item(
			Key = {
				'user_id':rowUserId
			}, 
			UpdateExpression="set interests = :r, last_tweet_id=:p, interests_count=:a",
		    ExpressionAttributeValues={
		        ':r': interests,
		        ':p': last_tweet_id,
		        ':a': len(interests)
		    },
		    ReturnValues="UPDATED_NEW"
		)
		print response

	# Apparently dynamo stores numerical data as Decimal(1231423134), which was raising exceptions while serializing
	# the data in json format.
	def formatContent(self, result):
		User = {
	        'user_id': int(result['user_id']),
	        'name': result['name'],
	        'screen_name': result['screen_name'],
	        'profile_image_url': result['profile_image_url'],
	        'location': result['location'],
	        'follower_count': int(result['follower_count']),
	        'friends_count': int(result['friends_count']),
	        'profile_url': result['profile_url'],
	        'description': result['description'],
	        'statuses_count': int(result['statuses_count']),
	        'interests': result['interests'],
	        'interests_count': int(result['interests_count']),
	        'last_tweet_id': int(result['last_tweet_id']),
		}
		return User


# Format for User :)
# 
# User = {
#         'user_id': user.id,
#         'name': user.name,
#         'screen_name': user.screen_name,
#         'profile_image_url': user.profile_image_url,
#         'location': user.location,
#         'follower_count': user.followers_count,
#         'friends_count': user.friends_count,
#         'profile_url': "http:/twitter.com/" + user.screen_name,
#         'description': user.description,
#         'statuses_count': user.statuses_count,
#         'interests': interests_list,
#         'interests_count': len(interests_list),
#         'last_tweet_id': last_tweet_id
# }

# dynamo = DynamoTable('default', 'twitty-users')
# result = dynamo.getUser(1412174058)
# mod = dynamo.formatContent(result)
# print mod 

# users = dict()



# for key in results:
# 	users[row['user_id']] = row

