from datetime import datetime, date
from typing import Optional, Dict, Any, List, Union

class Pessoa():
	id: Union[str, None] = None
	apelido: str = ''
	nome: str = ''
	stack: Union[List[str], None] = None
	nascimento: date = ''

	def __init__(self, data: List[Dict[str, Any]] = None):
		if data is None or len(data) == 0:
			return
		
		self.id = data[0]['id']
		self.apelido = data[0]['apelido']
		self.nome = data[0]['nome']
		self.nascimento = data[0]['nascimento']

		if 'stack' in data[0] and data[0]['stack'] is not None:
			self.stack: List[str] = []

			for element in data:
				self.stack.append(element['stack'])

	def serializer(obj):
		if isinstance(obj, Pessoa):
			return obj.__dict__

		if isinstance(obj, date):
			return obj.isoformat()
		
		raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
