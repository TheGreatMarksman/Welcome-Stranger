from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1 style='font-size: 3em'>Hello, World!</h1>"