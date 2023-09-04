import logging
import json
import uuid
from datetime import datetime

import flask
from flask import request, Response

import service.pessoa as PessoaService
from model.pessoa import Pessoa
import library.errors as errors

logger = logging.getLogger('Handler')

APELIDO_MAX_LENGTH = 32
NOME_MAX_LENGTH = 100
STACK_MAX_LENGTH = 32

def NewPessoa() -> Response:
	data = request.get_json(silent=True) #always consume body json data

	if not request.is_json:
		raise errors.BadRequest('the request body must be a json')

	if data is None:
		raise errors.BadRequest('invalid json')
	
	for field in ['apelido', 'nome', 'nascimento']:
		if not field in data or data[field] is None:
			raise errors.UnprocessableEntity(f'missing "{field}" field')
		
		if not isinstance(field, str):
			raise errors.BadRequest(f'field "{field}" must be a string')
		
	if 'stack' in data:
		if not isinstance(data['stack'], list):
			raise errors.BadRequest('field "stack" must be a list of strings')
		
		for stack in data['stack']:
			if not isinstance(stack, str):
				raise errors.BadRequest('field "stack" must be a list of strings')
			
			if len(stack) > STACK_MAX_LENGTH:
				raise errors.UnprocessableEntity(f'stacks must not have more than {STACK_MAX_LENGTH} characters')
	
	if len(data['apelido']) > APELIDO_MAX_LENGTH:
		raise errors.UnprocessableEntity(f'"apelido" field must not have more than {APELIDO_MAX_LENGTH} characters')
	
	if len(data['nome']) > NOME_MAX_LENGTH:
		raise errors.UnprocessableEntity(f'"nome" field must not have more than {NOME_MAX_LENGTH} characters')
	
	try:
		nascimento = datetime.strptime(data['nascimento'], '%Y-%m-%d').date()
	except ValueError:
		raise errors.BadRequest('"nascimento" field must be a date in the yyyy-mm-dd format')

	try:
		pessoa_id = PessoaService.Create(data['apelido'], data['nome'], nascimento, data['stack'])
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 201
	res.headers.add('Location', f'/pessoas/{pessoa_id}')

	return res

def GetPessoaByID(id: str) -> Response:
	try:
		uuid.UUID(id, version=1)
	except ValueError:
		raise errors.NotFound(f'pessoa with id "{id}" not found') #change it later

	try:
		pessoa = PessoaService.GetByID(id)
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	res.set_data(json.dumps(pessoa, ensure_ascii=False, default=Pessoa.serializer))

	return res

def FilterPessoas() -> Response:
	query = request.args.get('t')
	if query is None or query == '':
		raise errors.BadRequest('missing or empty "t" querystring parameter')

	try:
		pessoas = PessoaService.Filter(query)
	except:
		raise

	res = flask.make_response()
	res.content_type = 'application/json; charset=utf-8'
	res.status_code = 200
	res.set_data(json.dumps(pessoas, ensure_ascii=False, default=Pessoa.serializer))

	return res

def CountPessoas() -> Response:
	try:
		pessoas_quantity = PessoaService.Count()
	except:
		raise

	res = flask.make_response()
	res.content_type = 'text/plain; charset=utf-8'
	res.status_code = 200
	res.set_data(str(pessoas_quantity))

	return res
