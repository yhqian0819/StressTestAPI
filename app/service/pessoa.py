import logging
from datetime import date
from typing import List

import repository.pessoa as PessoaRepository
import library.errors as errors
from model.pessoa import Pessoa
from library.mysql import IntegrityError

logger = logging.getLogger('Pessoa Service')

def Create(apelido: str, nome: str, nascimento: date, stack: List[str]) -> str:
	pessoa = Pessoa()
	pessoa.apelido = apelido
	pessoa.nome = nome
	pessoa.nascimento = nascimento
	pessoa.stack = stack

	try:
		id = PessoaRepository.Create(pessoa)
	except IntegrityError:
		raise errors.UnprocessableEntity(f'"{apelido}" already exists in database')
	except:
		raise

	return id

def GetByID(id: str) -> Pessoa:
	try:
		pessoa = PessoaRepository.GetByID(id)
	except:
		raise

	if pessoa is None:
		raise errors.NotFound(f'pessoa with id "{id}" not found')
	
	return pessoa

def Filter(q: str) -> List[Pessoa]:
	try:
		pessoas = PessoaRepository.Filter(q)
	except:
		raise

	return pessoas

def Count() -> int:
	try:
		pessoas_quantity = PessoaRepository.Count()
	except:
		raise

	return pessoas_quantity
