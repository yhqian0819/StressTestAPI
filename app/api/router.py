import flask
from flask import Blueprint, request, render_template

import json
import logging

import api.handler as Handler
from library.errors import InternalError, BaseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Router")

api = Blueprint('api', __name__)

@api.route('/pessoas', methods=['POST'])
def NewPessoa():
	return Handler.NewPessoa()

@api.route('/pessoas/<string:id>', methods=['GET'])
def GetPessoaByID(id: str):
	return Handler.GetPessoaByID(id)

@api.route('/pessoas', methods=['GET'])
def FilterPessoas():
	return Handler.FilterPessoas()

@api.errorhandler(BaseError)
def handle_crafted_errors(e: BaseError):
	response = e.get_response()
	response.data = json.dumps({
		'error': {
			'code': e.code,
			'name': e.name,
			'description': e.description,
		},
	})
	response.content_type = 'application/json'
	response.charset = 'utf-8'

	return response

@api.errorhandler(Exception)
def handle_exception(e: Exception):
	logger.error(e, exc_info=1)
	return handle_crafted_errors(InternalError(e.__str__()))
