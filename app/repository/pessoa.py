import logging
import uuid
from typing import List, Optional

from library.mysql import MySQL, Query
from model.pessoa import Pessoa

logger = logging.getLogger('Pessoa Repository')

def GetByID(id: str) -> Optional[Pessoa]:
	query = f"""
		SELECT BIN_TO_UUID(p.id, 1) AS id, p.apelido, p.nome, p.nascimento, GROUP_CONCAT(ps.stack) AS stack
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE p.id = UUID_TO_BIN('{id}', 1)
		GROUP BY p.id
	"""
	# Not using prepared statement due to only performance focus

	try:
		result, _ = MySQL().execute(query)
	except:
		raise

	if len(result) == 0:
		return None

	return Pessoa(result[0])

def Filter(q: str) -> List[Pessoa]:
	query = f"""
		SELECT BIN_TO_UUID(p.id, 1) AS id, p.apelido, p.nome, p.nascimento, GROUP_CONCAT(ps.stack) AS stack
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE MATCH(p.busca) AGAINST('*{q}*' IN BOOLEAN MODE)
		GROUP BY p.id
		LIMIT 50
	"""
	# Not using prepared statement due to only performance focus

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
	
	search_field = f'{pessoa.apelido} {pessoa.nome} ' + ' '.join(pessoa.stack)

	# Not using prepared statement due to only performance focus
	queries.append(Query(
		query=f"""
			INSERT INTO stresstest.pessoa (id, apelido, nome, nascimento, busca)
			VALUES (UUID_TO_BIN('{random_uuid}', 1), '{pessoa.apelido}', '{pessoa.nome}', '{str(pessoa.nascimento)}', '{search_field}')
		"""
	))

	if len(pessoa.stack) > 0:
		query_values = ''
		for stack in pessoa.stack:
			query_values += f"(UUID_TO_BIN('{random_uuid}', 1), '{stack}'),"

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
		SELECT COUNT(id) AS quantity
		FROM stresstest.pessoa
	"""

	try:
		result, _ = MySQL().execute(query)
	except:
		raise

	if len(result) == 0:
		return 0

	return int(result[0]['quantity'])
