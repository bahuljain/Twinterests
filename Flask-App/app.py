# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import tweepy
from dynamo import DynamoTable
from interests import UserInterests
from collections import defaultdict

app = Flask(__name__, static_url_path='/static')
app.debug = True
consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"
callback_url = 'http://68e4ef4c.ngrok.io/home'
oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
print "Application Authorized! \n"
signedin = False

@app.route('/')
def index():
    return render_template('index.html')

# initiate authentication
@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    # Use sessions here 
    if signedin is True:
        # directly go to home page of user
        print "You are already signed!!"
    else:
        if request.method == 'POST':
            return redirect(oauth.get_authorization_url(signin_with_twitter=True))

# create access tokens
@app.route('/home', methods=['GET'])
def home(name=None):
    verifier = request.args.get('oauth_verifier')
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError as e:
        print e
    
    api = tweepy.API(oauth)
    user = api.me()
    print user.name + " has logged in."

    dynamo = DynamoTable('bkj2111', 'twitty-users')
    
    if dynamo.checkUserExists(user.id) is False:
        print "New User"
        processFirstTimeUser(api, dynamo)
    else:
        print "Existing User"
        processExistingUser(api, dynamo)    
    
    #sample_user = { 'id': '1234', 'interests': [{'id': '01','topic': 'soccer'}, {'id': '02','topic': 'baseball'}] }
    # all_users = dynamo.scanTable()
    # sample_user = [u for u in all_users if int(str(u['user_id'])) == user.id]
    # getMatches(sample_user, all_users)

    return render_template('home.html', name=user.name)   

def processFirstTimeUser(api, dynamo):
    user = api.me()

    interests = UserInterests(api, None)
    
    interests.generateInterests()
    interests_dict = interests.getInterests()
    print interests_dict
    
    print "\nEnriching Interests"
    interests.enrichTopicList()
    interests_dict = interests.getInterests()
    print interests_dict
    
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

def processExistingUser(api, dynamo):
    user = api.me()
    
    rowUser = dynamo.getUser(user.id)
    print "user fetched from db"

    interests_dict = rowUser["interests"]

    userInterests = UserInterests(api, interests_dict)
    success = userInterests.generateNewInterests(rowUser["last_tweet_id"])
    
    if success:
        print "update dynamo"

        last_tweet_id = user.status.id
        interests = userInterests.getInterests()
        
        dynamo.updateInterests(rowUser['user_id'], last_tweet_id, interests)        
    else:
        print 'No new updates'

def getMatches(user, all_users):
    list_of_matches = list() # List of tuples with format (key id, list of json objects of matching topics)
    
    match_value_dict = dict() # key is user id, value is number of matches
    match_topics_list_dict = defaultdict(list) # key is user id, value is list of topic matches

    for x in all_users: # Initialize all other users to have 0 matches
        if (x['id'] != user['id']):
            match_value_dict[x['id']] = 0

    for x in user['interests']: # Iterate user interests

        print '--- current user interest: ' + x['topic']
        for i in all_users: # Iterate all users
            if (i['id'] != user['id']):
            
                print '-- comparing with user id: ' + i['id']
                
                for j in i['interests']: # Iterate other users interests
                    
                    print 'other user interest: ' + j['topic']
                    if(j['id'] == x['id']):
                        print 'match found!'
                        match_value_dict[i['id']] += 1
                        print j['topic']
                        match_topics_list_dict[i['id']].append(j)

                
                    
#    print 'match_value_dict:'
#    print match_value_dict
#    
#    print 'match_topics_list_dict:'
#    print match_topics_list_dict   
                    
    tuple_list = list()
    
    for x in match_value_dict:
        tuple_list.append((x, match_value_dict[x]))

    for x in sorted(tuple_list, key=lambda tup: tup[1], reverse=True):
        list_of_matches.append((x[0], match_topics_list_dict[x[0]]))
        
    print 'final tuple list:'
    print list_of_matches
            
    return list_of_matches #in reverse similarity order

if __name__ == '__main__':
    app.run()
