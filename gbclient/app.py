from flask import Flask
from flask_cors import CORS, cross_origin
from settings import *

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config.from_pyfile('settings.py', silent=True)

if CORS_ENABLED:
    cors = CORS(app, **CORS_CONFIG)

@app.route('/')
def index():
    return '<h1>gbclient-unix</h1>' \
           'Accepting connections!'
