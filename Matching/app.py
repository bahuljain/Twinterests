from flask import Flask, render_template, request, redirect
from matcher import Matcher
import json

app = Flask(__name__, static_url_path='/static')
app.debug = True

@app.route('/')
def index():
	user_id = 1412174058
	data = Matcher(user_id)
	data.getUsersInfo()
	data.doMatching()
	graph = data.getUserMatchesGraph()
	nodes = graph[0]
	edges = graph[1]

	return render_template('index.html', nodes=json.dumps(nodes), edges=json.dumps(edges))


if __name__ == '__main__':
    app.run()