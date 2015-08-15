from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex
import sqlite3

class sqlistmodel(QAbstractListModel):
	def __init__(self, conn):
		super().__init__()
		self._conn = conn
		self._data = [(0, '')]
		self._rolesindex = {
			Qt.DisplayRole: 1, 
			Qt.UserRole: 0}
	def printData(self):
		print(self._data)
	def updateData(self, query):
		q = self._conn.cursor()
		q.execute(query)
		self.beginResetModel()
		self._data = q.fetchall()
		self.endResetModel()
	def rowCount(self, parent=QModelIndex()):
		return len(self._data)
	def data(self, index, role):
		if not index.isValid():
			return None
		if index.row() >= len(self._data):
			return None
		if role in self._rolesindex.keys():
			return self._data[index.row()][self._rolesindex[role]]
		else:
			return None
	def roleNames(self):
		return {Qt.DisplayRole: b"name",
			Qt.UserRole: b"uid"}
class playlistmodel(sqlistmodel):
	def __init__(self, conn):
		QAbstractListModel.__init__(self)
		self._conn = conn
		self._data = [('', '', 0)]
		self._rolesindex = {
			Qt.DisplayRole: 0, 
			Qt.UserRole: 1,
			Qt.UserRole+1: 2}
	def roleNames(self):
		return {Qt.DisplayRole: b"name",
			Qt.UserRole: b"url",
			Qt.UserRole+1: b"uid"}
	def recordPlayed(self, uid):
		q = self._conn.cursor()
		q.execute('SELECT timesplayed,album FROM songs WHERE id=?', (uid,))
		times,album = q.fetchone()
		if times is None:
			times = 0
		q.execute("""UPDATE songs SET lastplayed=strftime('%s','now'),
			timesplayed=? WHERE id=?""",(times+1,uid))
		q.execute("""UPDATE albums SET lastplayed=strftime('%s','now')
			WHERE id=?""",(album,))
		self._conn.commit()
	def recordSkipped(self, uid):
		q = self._conn.cursor()
		q.execute('SELECT timesskipped FROM songs WHERE id=?', (uid,))
		times = q.fetchone()[0]
		if times is None:
			times = 0
		q.execute("UPDATE songs SET timesskipped=? WHERE id=?",(times+1,uid))
		self._conn.commit()
