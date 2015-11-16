import json

result = {u'topics': [{u'topic': u'Machine Learning', u'score': 0.75085, u'id': 2620}, {u'topic': u'Pattern Recognition', u'score': 0.74788, u'id': 30489}, {u'topic': u'Artificial Intelligence', u'score': 0.72795, u'id': 308}, {u'topic': u'Neural Networks', u'score': 0.71166, u'id': 28635}, {u'topic': u'Learning Theory', u'score': 0.69553, u'id': 24158}, {u'topic': u'Cognitive Science', u'score': 0.66557, u'id': 986}, {u'topic': u'Data Mining', u'score': 0.64779, u'id': 1161}]}
result2 = {u'topics': [{u'topic': u'Laptops', u'score': 0.41361, u'id': 23948}, {u'topic': u'Mac OS X', u'score': 0.29805, u'id': 25330}]}

topics = result['topics']

for topic in topics:
    print topic
