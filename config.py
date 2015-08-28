import sqlite3

class configHandler():
	def __init__(self,conn):
		self._conn = conn
		self._config = {}
		q = self._conn.cursor()
		q.execute("SELECT * FROM config")
		for (key, val) in q.fetchall():
			self._config[key]=val
	def get(self, key):
		if key in self._config.keys():
			return self._config[key]
		else:
			return None
	def set(self, key, val):
		q = self._conn.cursor()
		q.execute("INSERT OR REPLACE INTO config VALUES (?,?)",
				(key,val))
		self._config[key]=val
		self._conn.commit()
