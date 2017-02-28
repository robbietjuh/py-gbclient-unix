from flask import Flask
from settings import *

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config.from_pyfile('settings.py', silent=True)


@app.route('/')
def index():
    return '<h1>gbclient-unix</h1>' \
           'Accepting connections!'
