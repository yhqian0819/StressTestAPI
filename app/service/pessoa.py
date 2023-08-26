import logging
import datetime
from typing import List, Dict, Tuple, Optional

import repository.pessoa as PessoaRepository
import library.errors as errors
from model.pessoa import Pessoa
from library.mysql import IntegrityError

logger = logging.getLogger('Pessoa Service')

def Create(apelido: str, nome: str, nascimento: datetime.date, stack: List[str]) -> str:
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
