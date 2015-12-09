# -*- coding: utf-8 -*-
from collections import defaultdict

sample_user = { 'id': '1234', 'interests': [{'id': '01','topic': 'soccer'}, {'id': '02','topic': 'baseball'}] }
    
sample_other = [
    {
        'id': '1234',
        'interests': [{'id': '01','topic': 'soccer'}, {'id': '03','topic': 'hockey'}]
    },

    {
        'id': '1235',
        'interests': [{'id': '01','topic': 'soccer'}, {'id': '02','topic': 'baseball'}]
    },
    
    {
        'id': '1236',
        'interests': [{'id': '01','topic': 'soccer'}, {'id': '04','topic': 'Volleyball'}, {'id': '03','topic': 'hockey'}]
    }
]

#sample_other = []


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


getMatches(sample_user, sample_other)