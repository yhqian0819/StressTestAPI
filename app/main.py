import eventlet
eventlet.monkey_patch()

import flask
from flask import Flask, request
from werkzeug.exceptions import HTTPException

import json
import logging

from api.router import api as API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

app = Flask(__name__)

app.register_blueprint(API)
app.templates_auto_reload = True

#if __name__ == '__main__':
	#app.run("0.0.0.1", "5000")
	#logging.basicConfig(filename='myapp.log', level=logging.INFO)
