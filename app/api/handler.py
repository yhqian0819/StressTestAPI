import logging
import json
import os
import flask
from flask import request, render_template, redirect, Response

import service.service as srv
import library.errors as errors

logger = logging.getLogger('Handler')

def Translate():
	if not request.is_json:
		raise errors.BadRequest('json inválido')

	data = request.get_json()
	if data is None:
		raise errors.BadRequest('json inválido')

	if not 'text' in data:
		raise errors.BadRequest('missing text to translate')

	if not isinstance(data['text'], str):
		raise errors.BadRequest('invalid payload text field type')

	try:
		translation = srv.Translate(data['text'])
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	res.set_data(json.dumps({'translation': translation}))

	return res
