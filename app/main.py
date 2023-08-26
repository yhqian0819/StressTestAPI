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

"""@app.errorhandler(HTTPException)
def handle_crafted_errors(e: HTTPException):
	response = e.get_response()
	response.data = json.dumps({
		"code": e.code,
		"name": e.name,
		"description": e.description,
	})
	response.content_type = "application/json"
	response.charset = 'utf-8'

	return response

@app.errorhandler(Exception)
def handle_exception(e: Exception):
	logger.error(e, exc_info=1)
	return handle_crafted_errors(InternalError(e.__str__()))"""

#if __name__ == '__main__':
	#app.run("0.0.0.1", "5000")
	#logging.basicConfig(filename='myapp.log', level=logging.INFO)
