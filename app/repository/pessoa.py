import logging
import uuid
from typing import List, Optional, Dict

from library.mysql import MySQL, Query
from model.pessoa import Pessoa

import library.errors as errors

logger = logging.getLogger('Pessoa Repository')

def GetByID(id: str) -> Optional[Pessoa]:
	query = f"""
		SELECT BIN_TO_UUID(p.id) AS id, p.apelido, p.nome, p.nascimento, GROUP_CONCAT(ps.stack)
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE p.id = UUID_TO_BIN('{id}')
	"""
	# Not using prepared statement due to only perfomance focus

	try:
		result, _ = MySQL().execute(query)
	except:
		raise

	if len(result) == 0:
		return None

	return Pessoa(result[0])

def Filter(q: str) -> List[Pessoa]:
	query = f"""
		SELECT BIN_TO_UUID(p.id) AS id, p.apelido, p.nome, p.nascimento, GROUP_CONCAT(ps.stack)
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE
			MATCH(p.apelido, p.nome) AGAINST('*{q}*' IN BOOLEAN MODE)
			OR
			(
				SELECT MAX(MATCH(ps2.stack) AGAINST('*{q}*' IN BOOLEAN MODE))
				FROM stresstest.pessoa_stacks ps2
				WHERE ps2.pessoa_id = p.id
			)
		GROUP BY p.id
		LIMIT 50
	"""
	# Not using prepared statement due to only perfomance focus

	try:
		result, _ = MySQL().execute(query)
	except:
		raise
	
	pessoas: List[Pessoa] = []
	for row in result:
		pessoas.append(Pessoa(row))

	return pessoas

def Create(pessoa: Pessoa) -> str:
	random_uuid = str(uuid.uuid4())
	queries: List[Query] = []

	# Not using prepared statement due to only perfomance focus
	queries.append(Query(
		query=f"""
			INSERT INTO stresstest.pessoa (id, apelido, nome, nascimento)
			VALUES (UUID_TO_BIN('{random_uuid}'), '{pessoa.apelido}', '{pessoa.nome}', '{str(pessoa.nascimento)}')
		"""
	))

	if len(pessoa.stack) > 0:
		query_values = ''
		for stack in pessoa.stack:
			query_values += f"(UUID_TO_BIN('{random_uuid}'), '{stack}'),"

		queries.append(Query(
			query=f"""
				INSERT INTO stresstest.pessoa_stacks (pessoa_id, stack)
				VALUES {query_values[:-1]}
			"""
		))

	try:
		MySQL().executeTxQueries(queries)
	except:
		raise

	return random_uuid

def Count() -> int:
	query = """
		SELECT COUNT(*) AS quantity
		FROM stresstest.pessoa
	"""

	try:
		result, _ = MySQL().execute(query)
	except:
		raise

	if len(result) == 0:
		return 0

	return int(result[0]['quantity'])
