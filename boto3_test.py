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
		reponse = self.table.put_item(User)
		print reponse

	def checkUserExists(self, id):
		response = self.table.query(
	    	KeyConditionExpression=Key('id').eq(id)
		)
		return True if response['Count'] > 0 else False

dynamoTable = DynamoTable('bkj2111', 'users')
# print dynamoTable.checkUserExists('1123')
print dynamoTable.scanTable()

# scanTable(tableName)

# Format for User :)

# response = table.put_item(
#    User={
#         'user_id':user_id,
#         'name':name,
#         'profile_image_url':profile_image_url,
#         'location':location,
#         'follower_count':follower_count,
#         'friends_count':friends_count,
#         'profile_url':profile_url,
#         'description':decription,
#         'statuses_count':statuses_count
#         'interests':interests,
#         'last_tweet_id':last_tweet_id
#     }
# )