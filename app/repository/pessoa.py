import logging
from typing import List, Optional

from library.mysql import MySQL
from model.pessoa import Pessoa

import library.errors as errors

logger = logging.getLogger('Pessoa Repository')

def GetByID(id: str) -> Optional[Pessoa]:
	query = """
		SELECT p.id, p.apelido, p.nome, p.nascimento, ps.stack
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE p.id = ?
	"""

	try:
		result, _ = MySQL().execute(query, (id,), usePrepared=True)
	except:
		raise

	if len(result) == 0:
		return None

	return Pessoa(result)

def Filter(q: str) -> List[Pessoa]:
	query_filter = q + ' IN BOOLEAN MODE'

	query = """
		SELECT *
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE
			MATCH(p.apelido * 1, p.nome * 1) AGAINST(?) OR
			MATCH(ps.stack) AGAINST(?)
		LIMIT 50
	"""

	try:
		result, _ = MySQL().execute(query, (query_filter,query_filter,), usePrepared=True)
	except:
		raise

	pessoas: List[Pessoa] = []

	for row in result:
		pessoas.append(Pessoa(row))

	return pessoas

def Create(pessoa: Pessoa) -> str:
	query = """
		INSERT INTO stresstest.pessoa (apelido, nome, nascimento)
		VALUES (?, ?, ?)
	"""

	try:
		_, pessoa_id = MySQL().execute(query, (pessoa.apelido, pessoa.nome, pessoa.nascimento,), usePrepared=True)
	except:
		raise

	if pessoa_id is None:
		try:
			MySQL().rollback()
		except:
			raise

		raise Exception('failed to create Pessoa')

	stacks_query = """
		INSERT INTO stresstest.pessoa (pessoa_id, stack)
		VALUES (?, ?)
	"""

	for stack in pessoa.stack:
		try:
			MySQL().execute(stacks_query, (pessoa_id, stack,), usePrepared=True)

		except Exception as e:
			logger.warning(f'could not create pessoa stack: {e}. Skipping...')
			continue

	return pessoa_id
