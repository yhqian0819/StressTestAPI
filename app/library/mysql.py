import os
import logging
from threading import Lock
from typing import List, Optional, Tuple, Callable

import mysql.connector.pooling as dbConnector
from mysql.connector.cursor import MySQLCursor, MySQLCursorPrepared, MySQLCursorDict
from mysql.connector.errors import Error as DBError, InterfaceError, InternalError, IntegrityError, Warning as DBWarning
#from mysql.connector import connection as dbConnection

logger = logging.getLogger("MYSQL")

class Query():
	def __init__(self, query: str, params: tuple = (), usePrepared: bool = False) -> None:
		self.query = query
		self.params = params
		self.usePrepared = usePrepared

class MySQL:
	_pool = None

	def __init__(self):
		if MySQL._pool is None:
			logger.info('new database connection pool')

			try:
				MySQL._pool = dbConnector.MySQLConnectionPool(
					pool_name=os.getenv('MYSQL_POOL_NAME'),
					pool_size=int(os.getenv('MYSQL_POOL_SIZE')),
					host=os.getenv('MYSQL_HOST'),
					user=os.getenv('MYSQL_USER'),
					password=os.getenv('MYSQL_PASSWORD'),
					raise_on_warnings=True, 
					autocommit=False,
					charset='utf8',
					use_unicode=True,
					time_zone='-03:00',
				)
			
			except DBError as err:
				logger.error('cannot connect to database: {}'.format(err.msg))
				raise

	def execute(self, query: str, params: tuple = (), usePrepared: bool = False, autoCommit: bool = True) -> Tuple[list, Optional[int]]:
		connection: dbConnector.PooledMySQLConnection = self._pool.get_connection()
		
		c_class = MySQLCursorDict
		if usePrepared and params != ():
			c_class = MySQLCursorPrepared

		cursor = connection.cursor(cursor_class=c_class)

		try:
			result, column_names, last_inserted_id = execute(cursor, query, params)
		
		except:
			self._rollback(connection)
			raise
		
		else:
			if autoCommit:
				self._commit(connection)

		finally:
			cursor.close()
			connection.close()

		response = []
		for row in result:
			if c_class == MySQLCursorPrepared:
				r = dict(zip(column_names, row))
				for key in r:
					try:
						r[key] = r[key].decode()
					except (UnicodeDecodeError, AttributeError):
						pass
					
				response.append(r)
			else:
				response.append(row)

		return response, last_inserted_id

	# Only for insert, update or delete queries
	def executeTxQueries(self, queries: List[Query], do_after_each: Callable = None) -> None:
		connection: dbConnector.PooledMySQLConnection = self._pool.get_connection()

		try:
			for query in queries:
				c_class = MySQLCursorDict
				if query.usePrepared and query.params != ():
					c_class = MySQLCursorPrepared

				cursor = connection.cursor(cursor_class=c_class)

				try:
					execute(cursor, query.query, query.params)

				except:
					raise

				else:
					if do_after_each is not None:
						do_after_each(query)
				
				finally:
					cursor.close()

		except:
			self._rollback(connection)
			raise

		else:
			self._commit(connection)

		finally:
			connection.close()
	
	def query(self, query: str, params: tuple = (), usePrepared: bool = False) -> Query:
		return Query(query, params, usePrepared)
	
	def _rollback(self, connection: dbConnector.PooledMySQLConnection):
		try:
			connection.rollback()
		
		except (DBError, InternalError, InterfaceError) as err:
			logger.debug('error trying to rollback transaction: {}'.format(err.msg))
			raise

	def _commit(self, connection: dbConnector.PooledMySQLConnection):
		try:
			connection.commit()

		except (DBError, InternalError, InterfaceError) as err:
			logger.debug('error trying to commit transaction: {}'.format(err.msg))
			raise

def execute(cursor: MySQLCursor, query: str, params: tuple) -> Tuple[list, tuple, Optional[int]]:
	try:
		cursor.execute(query, params, multi=False)

	except DBWarning as warn:
		logger.warning(warn.msg)
	
	except DBError as err:
		logger.debug('error executing query "{}" with args "{}": {}'.format(query, params, err.msg))
		raise

	column_names = cursor.column_names
	last_inserted_id = cursor.lastrowid

	try:
		result = cursor.fetchall()
		
	except InterfaceError as err:
		if err.msg == "No result set to fetch from" or err.msg == "No result set to fetch from.":
			return [], (), last_inserted_id
		
		raise
	
	return result, column_names, None
