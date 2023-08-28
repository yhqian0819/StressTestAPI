import logging
import uuid
from typing import List, Optional

from library.mysql import MySQL, Query
from model.pessoa import Pessoa

import library.errors as errors

logger = logging.getLogger('Pessoa Repository')

def GetByID(id: str) -> Optional[Pessoa]:
	query = """
		SELECT BIN_TO_UUID(p.id) AS id, p.apelido, p.nome, p.nascimento, ps.stack
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE p.id = UUID_TO_BIN(?)
	"""

	try:
		result, _ = MySQL().execute(query, (id,), usePrepared=True)
	except:
		raise

	if len(result) == 0:
		return None

	return Pessoa(result)

def Filter(q: str) -> List[Pessoa]:
	query_filter = f'*{q}*'

	query = """
		SELECT BIN_TO_UUID(p.id) AS id, p.apelido, p.nome, p.nascimento, ps.stack
		FROM stresstest.pessoa AS p
		LEFT JOIN stresstest.pessoa_stacks AS ps ON (ps.pessoa_id = p.id)
		WHERE
			MATCH(p.apelido, p.nome) AGAINST(? IN BOOLEAN MODE) OR
			MATCH(ps.stack) AGAINST(? IN BOOLEAN MODE)
		LIMIT 50
	"""

	try:
		result, _ = MySQL().execute(query, (query_filter, query_filter,), usePrepared=True)
	except:
		raise
	
	pessoas: List[Pessoa] = []

	result_length = len(result)
	if result_length == 0:
		return pessoas

	current_pessoa_id = result[0]['id']
	current_pessoa_rows = []
	
	for i, row in enumerate(result):
		if row['id'] == current_pessoa_id:
			current_pessoa_rows.append(row)

			if i < result_length - 1:
				continue

		pessoas.append(Pessoa(current_pessoa_rows))
		current_pessoa_id = row['id']
		current_pessoa_rows = [row]

	return pessoas

def Create(pessoa: Pessoa) -> str:
	random_uuid = str(uuid.uuid4())
	queries: List[Query] = []

	queries.append(Query(
		query=f"""
			INSERT INTO stresstest.pessoa (id, apelido, nome, nascimento)
			VALUES (UUID_TO_BIN('{random_uuid}'), ?, ?, ?)
		""",
		params=(pessoa.apelido, pessoa.nome, pessoa.nascimento,),
		usePrepared=True,
	))

	args = []
	query_values = ''
	for stack in pessoa.stack:
		args.append(stack)
		query_values += f"(UUID_TO_BIN('{random_uuid}'), ?),"

	if len(pessoa.stack) > 0:
		queries.append(Query(
			query=f"""
				INSERT INTO stresstest.pessoa_stacks (pessoa_id, stack)
				VALUES {query_values[:-1]}
			""",
			params=tuple(args),
			usePrepared=True,
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
