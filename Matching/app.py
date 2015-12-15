from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')
app.debug = True

@app.route('/')
def index():
    return 'Hello World'#render_template('index.html')


if __name__ == '__main__':
    app.run()
