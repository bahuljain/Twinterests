import csv
import json
# total number of users

class Matcher:

    def __init__(self):
        self.usersInfo = list()
        self.nodes = list()
        self.edges = list()

    def getUsersInfo(self):
        with open('db/twitty-users.csv','rb') as fin:
            dr = csv.DictReader(fin)
            for row in dr:
            	self.usersInfo.append(row)
        
    def getUsersCount(self):
        return len(self.usersInfo)

    def getMatches(self):
        # print self.usersInfo[0]['interests (M)']
        for i in range(0,self.getUsersCount()-1):
            self.match(self.usersInfo[i], self.usersInfo[i+1:])
            # for j in range(i+1, self.getUsersCount()):
                # compare user[i] with all users from i to end           


    def match(self, cur_user, all_users):
        self.nodes.append({
            'id': int(cur_user['user_id (N)']), 
            'title': cur_user['name (S)'], 
            'image': cur_user['profile_image_url (S)']
        });

        for user in all_users:
            commonInterests = self.getCommonInterests(cur_user['interests (M)'], user['interests (M)'])
            
            if len(commonInterests) > 0:
                title = ', '.join(commonInterests[id]['S'] for id in commonInterests)
                self.edges.append({
                    'from': int(cur_user['user_id (N)']),
                    'to': int(user['user_id (N)']), 
                    'title': title
                });

    def getCommonInterests(self, dict1, dict2):
        dict1 = json.loads(dict1)
        dict2 = json.loads(dict2)
     
        commonInterests = dict()
        for id in dict1:
            if id in dict2:
                commonInterests[id] = dict1[id]
                
        return commonInterests    

    def getNodes(self):
        return self.nodes
        # for node in self.nodes:
        #     print node['id'] + ": " + node['title']
        

    def getEdges(self):
        return self.edges
        # for edge in self.edges:
        #     if edge['from'] == 174153942 or edge['to'] == 174153942:
        #         print `edge['from']` + ' -> ' + `edge['to']` + ' : ' + `edge['title']`
            

matcher = Matcher()
matcher.getUsersInfo()
matcher.getMatches()
# matcher.getNodes()
matcher.getEdges()
