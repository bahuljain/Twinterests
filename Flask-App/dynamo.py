import boto3.session
from boto3.dynamodb.conditions import Key, Attr

class DynamoTable:

	def __init__(self, profileName, tableName):
		self.boto3 = boto3.session.Session(profile_name=profileName)
		self.dynamo = self.boto3.resource('dynamodb', 'us-east-1')
		self.table = self.dynamo.Table(tableName)

	def scanTable(self):
		result = self.table.scan()
		print "Fetched: " + `result['Count']` + " Users" 
		return result["Items"]

	def addUserToDB(self, User):
		response = self.table.put_item(Item=User)

	def checkUserExists(self, id):
		response = self.table.query(
	    	KeyConditionExpression=Key('user_id').eq(id)
		)
		return True if response['Count'] > 0 else False

	def getUser(self, id):
		result = self.table.query(
			KeyConditionExpression=Key('user_id').eq(id)
		)
		return result['Items'][0] if result['Count'] > 0 else None

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
