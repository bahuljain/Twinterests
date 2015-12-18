# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import tweepy
from dynamo import DynamoTable
from interests import UserInterests
from collections import defaultdict
from matcher import Matcher
import json

app = Flask(__name__, static_url_path='/static')
app.debug = True
consumer_key = "VlFNycQDt1xgm1w7ggatd748Q"
consumer_secret = "NKfuFXkIcIQNdMtOpim2TJ1avcwXuOCsAOVcR7gl9AQa5dQ1JS"
callback_url = 'http://3ac49772.ngrok.io/auth'
session = dict()
db = dict()

# Return the home page of the application.
@app.route('/')
def index():
    return render_template('index.html')

# initiate authentication by logging in the user via twitter.
@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    if request.method == "POST":
        oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
        redirect_url = oauth.get_authorization_url(signin_with_twitter=True)
        session['request_token'] = oauth.request_token

        # Android Application
        if request.form.get('device', type=str) is "mobile":
            session['device'] = "mobile"
            return redirect_url
        
        # Web Application
        else:
            session['device'] = "web"
            return redirect(redirect_url)

# create access tokens and redirect to user home page :)
@app.route('/auth', methods=['GET'])
def auth():
    verifier = request.args.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

    oauth.request_token = session['request_token']
    del session['request_token']

    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError as e:
        print e

    api = tweepy.API(oauth)
    
    if api.me().id not in db.keys():
        db[api.me().id] = {'api': api}

    print api.me().name + " has logged in."

    return redirect(url_for('home', user_id=api.me().id))   

# Home Screen for the User. 
# check if the user is in database and accordingly process the user.
# also the matcher is created. We perform a full matching of all the users in the database. 
@app.route('/home', methods=['GET', 'POST'])
def home():
    id = request.args.get('user_id')
    api = db[int(id)]['api']
    user = api.me()

    dynamo = DynamoTable('default', 'twitty-users')
    
    if dynamo.checkUserExists(user.id) is False:
        print "New User"
        interests = processFirstTimeUser(api, dynamo)
        db[user.id]['interests'] = interests
    else:
        print "Existing User"
        interests = processExistingUser(api, dynamo)    
        db[user.id]['interests'] = interests
    
    # do matching here now!!
    if 'matcher' not in db.keys():
        print "Begin Matching"
        items = dynamo.scanTable()

        users = dict()
        for item in items:
            users[item['user_id']] = dynamo.formatContent(item)

        matcher = Matcher(items, users)
        matcher.doMatching()

        db['matcher'] = matcher
        db['users'] = users
        print "Matching Done"

    if session['device'] is "mobile":
        del session['device']
        return redirect(url_for('dashboard', user_id=id, device="mobile"))
    else:
        del session['device']
        return render_template('home.html', name=user.name, user_id=id)

# Return current user information, list of users sharing interests with the current user, including
# their individual information and common interests
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # print "Received Request"
    id = int(request.args.get('user_id'))
    device = request.args.get('device')
    # id = request.form.get('user_id', type=int)
    api = db[id]['api']
    user = api.me()
    # user = api.get_user('prakharsriv9')

    matcher = db['matcher']
    users = db['users']

    matches = matcher.getUserMatches(user.id)

    matchingUsers = dict()
    for match in matches:
        to = match['with'] 
        matchingUsers[to] = {'userDetails': users[to], 'commonInterests': match['interests']}

    # Android Application
    if device is "mobile":
        return json.dumps({
            'user_id': user.id,
            'name': user.name,
            'user': users[user.id],
            'matchingUsers': cleanDict(matchingUsers),
        })

    # Web Application
    else:
        return render_template('dashboard.html',
            name=user.name, 
            user_id=user.id, 
            user=json.dumps(users[user.id]),
            matchingUsers=json.dumps(cleanDict(matchingUsers))
        )

# Return nodes and edges for the entire twitter graph!! :)
@app.route('/twitterGraph', methods=['GET'])
def twitterGraph():
    id = request.args.get('user_id')
    matcher = db['matcher']
    graph = matcher.getTwitterGraph()
    nodes = graph[0]
    edges = graph[1]

    print len(edges)

    device = request.args.get('device')
    
    # Web Application
    if device is "web":
        return render_template('twitter-graph.html',
            user_id=id, 
            nodes=json.dumps(nodes), 
            edges=json.dumps(edges),
            graph=1
        )

    # Android Application 
    else:
        return None

# Return the nodes and edges for the user's social graph, depicting all the users he/she shares 
# common interest with.
@app.route('/socialGraph', methods=['GET'])
def socialGraph():
    id = request.args.get('user_id')
    matcher = db['matcher']
    # print id
    graph = matcher.getUserSocialGraph(int(id))
    nodes = graph[0]
    edges = graph[1]

    print len(nodes)
    print len(edges)


    return render_template('twitter-graph.html', 
        user_id=id, 
        nodes=json.dumps(nodes), 
        edges=json.dumps(edges),
        graph=2
    )

# Logout user!!
@app.route('/logout', methods=['GET'])
def logout():
    id = int(request.args.get('user_id'))

    del db[id]
    
    device = str(request.args.get('device'))

    # Web Application
    if device == 'web':
        return redirect(url_for('index'))
    
    # Android Application
    else:
        return None

# 1. First of all generate the interests of the user.
# 2. Enrich the interests list of the user in case there arent many interests of the user.
# 3. Add the user to the database.
def processFirstTimeUser(api, dynamo):
    user = api.me()

    interests = UserInterests(api, None)
    
    last_tweet_id = interests.generateInterests()
    interests_dict = interests.getInterests()
    print interests_dict
    
    print "\nEnriching Interests"
    interests.enrichTopicList()
    interests_dict = interests.getInterests()
    print interests_dict
    
    print "interests generated"

    print "Last Tweet ID: " + `last_tweet_id`

    dynamo.addUserToDB(user, interests_dict, last_tweet_id)

    return interests_dict

# 1. Fetch user from database.
# 2. Generate new interests of user from his/her new and recent tweets.
# 3. Update new interests in the database.
def processExistingUser(api, dynamo):
    user = api.me()
    
    rowUser = dynamo.getUser(user.id)
    print "user fetched from db"

    interests_dict = rowUser["interests"]

    userInterests = UserInterests(api, interests_dict)
    response = userInterests.generateNewInterests(rowUser["last_tweet_id"])
    
    if response[0]:
        print "update dynamo"

        last_tweet_id = response[1]
        interests = userInterests.getInterests()
        
        dynamo.updateInterests(rowUser['user_id'], last_tweet_id, interests)        
    else:
        print 'No new updates'

    return userInterests.getInterests()

# Some keys were not string which was hindering the dumps function from serializing the data, hence the cleaning required.
def cleanDict(dictionary):
    for key in dictionary.keys():
        if type(key) is not str:
            dictionary[str(key)] = dictionary[key]
            del dictionary[key]

    return dictionary

if __name__ == '__main__':
    app.run()

