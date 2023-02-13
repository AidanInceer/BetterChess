import time

from flask import Flask

app = Flask(__name__)


@app.route("/")
def get_current_time():
    return {"time": time.time()}


@app.route("/home")
def home_page():
    return "homepage"
