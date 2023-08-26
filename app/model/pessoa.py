import datetime
from typing import Optional, Dict, Any, List

class Pessoa():
	id: str | None = None
	apelido: str = ''
	nome: str = ''
	stack: List[str] | None = None
	nascimento: datetime.date = ''

	def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
		if data is not None and len(data) > 0:
			self.id = data[0]['id']
			self.apelido = data[0]['apelido']
			self.nome = data[0]['nome']
			self.nascimento = datetime.date.fromisoformat(data[0]['nascimento'])

			if 'stack' in data[0] and data[0]['stack'] is not None:
				self.stack: List[str] = []

				for element in data:
					self.stack.append(element['stack'])

	def serializer(obj):
		if isinstance(obj, Pessoa):
			return obj.__dict__

		if isinstance(obj, datetime.date):
			return obj.isoformat()
		
		raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
