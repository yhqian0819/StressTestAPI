from datetime import datetime, date
from typing import Optional, Dict, Any, List, Union

class Pessoa():
	id: Union[str, None] = None
	apelido: str = ''
	nome: str = ''
	stack: Union[List[str], None] = None
	nascimento: date = ''

	def __init__(self, data: Dict[str, Any] = None):
		if data is None:
			return
		
		self.id = data['id']
		self.apelido = data['apelido']
		self.nome = data['nome']
		self.nascimento = data['nascimento']

		if 'stack' in data:
			self.stack = data['stack'].split(',')

	def serializer(obj):
		if isinstance(obj, Pessoa):
			return obj.__dict__

		if isinstance(obj, date):
			return obj.isoformat()
		
		raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
