#
# This file is part of chirpy
# (c) 2015 Felix Braun
# for licensing information see the file LICENSE
#

import sqlite3

class mediabase:
	def __init__(self, filename):
		self._conn = sqlite3.connect(filename)
		self._conn.isolation_level = "EXCLUSIVE"
		q = self._conn.cursor()
		q.executescript("""
	CREATE TABLE IF NOT EXISTS config (
		key	TEXT PRIMARY KEY,
		value	TEXT
		) WITHOUT ROWID;
	CREATE TABLE IF NOT EXISTS songs (
		id	INTEGER PRIMARY KEY,
		album	INTEGER REFERENCES albums(id),
		trackno	INTEGER,
		name	TEXT,
		path	TEXT UNIQUE ON CONFLICT ROLLBACK,
		rating	INTEGER,
		timesplayed INTEGER,
		timesskipped INTEGER,
		lastplayed DATETIME,
		filectime DATETIME
		);
	CREATE UNIQUE INDEX IF NOT EXISTS pathidx ON songs (path);
	CREATE TABLE IF NOT EXISTS albums (
		id	INTEGER PRIMARY KEY,
		category INTEGER REFERENCES categories(id),
		name	TEXT,
		trackcount INTEGER,
		datetime DATE
		);
	CREATE INDEX IF NOT EXISTS albumidx ON albums (name);
	CREATE TABLE IF NOT EXISTS artists (
		id	INTEGER PRIMARY KEY,
		name	TEXT
		);
	CREATE INDEX IF NOT EXISTS artistidx ON artists (name);
	CREATE TABLE IF NOT EXISTS song_artists (
		song_id	INTEGER REFERENCES songs(id),
		artist_id INTEGER REFERENCES artists(id),
		artist_type  INTEGER
		);
	CREATE TABLE IF NOT EXISTS genres (
		id	INTEGER PRIMARY KEY,
      		name	TEXT
		);
	CREATE TABLE IF NOT EXISTS song_genres (
		song_id	INTEGER REFERENCES songs(id),
		genre_id INTEGER REFERENCES genres(id)
		);
	CREATE TABLE IF NOT EXISTS categories (
		id	INTEGER PRIMARY KEY,
		name	TEXT
		);
	""")
		self._conn.commit()
		self._conn.isolation_level="DEFERRED"
	def addObj(self, mo):
		(song_id,basetime)=self.getCTime(mo['path'][0])
		if basetime > 0 and mo['ctime'][0] == basetime:
			return
		q = self._conn.cursor()
		for key in ['album', 'title', 'artist', 'genre']:
			if key not in mo.keys():
				mo[key]=['Unknown']
		mo['album'][0] = self.getId('albums', mo['album'][0])
		columns = ["album","name","path","filectime"]
		values = [mo['album'][0], mo['title'][0], mo['path'][0], mo['ctime'][0]]
		if 'track-number' in mo.keys():
			columns.append('trackno')
			values.append(mo['track-number'][0])
		if song_id == 0:
			para = "?"+",?"*(len(columns)-1)
			q.execute("INSERT INTO songs("+",".join(columns)+") VALUES ("+para+")", tuple(values))
			song_id = q.lastrowid
		else:
			para = str()
			for i in range(len(columns)):
				para = para+""+columns[i]+"=?"+","
			para = para[:-1]
			query = "UPDATE songs SET "+para+" WHERE id="+str(song_id)
			q.execute(query, tuple(values))
		q.execute("SELECT artist_id FROM song_artists WHERE song_id = ?",(song_id,))
		old = set(q.fetchall())
		new = set()
		for artist in mo['artist']:
			new.add((self.getId('artists',artist),))
		for artist in new - old:
			artist = artist[0]
			q.execute("INSERT INTO song_artists VALUES (?, ?, ?)", (song_id, artist, 1))
		for artist in old - new:
			artist = artist[0]
			q.execute("DELETE FROM song_artists WHERE (song_id = ?) AND (artist_id = ?)", (song_id, artist))

		q.execute("SELECT genre_id FROM song_genres WHERE song_id = ?", (song_id,))
		old = set(q.fetchall())
		new = set()
		for genre in mo['genre']:
			new.add((self.getId('genres',genre),))
		for genre in new - old:
			genre = genre[0]
			q.execute("INSERT INTO song_genres VALUES (?, ?)", (song_id, genre))
		for genre in old - new:
			genre = genre[0]
			q.execute("DELETE FROM song_genres WHERE (song_id = ?) AND (genre_id = ?)", (song_id, genre))
		self._conn.commit()
	def deleteUnreferenced(self, table1, table2, ref):
		q = self._conn.cursor()
		q.execute("SELECT id FROM "+table1+" EXCEPT SELECT DISTINCT "+
			ref+" FROM "+table2)
		not_needed = q.fetchall()
		for row in not_needed:
			q.execute("DELETE FROM "+table1+" WHERE id = ?",row)
		if not_needed is not None:
			self._conn.commit()
	def getId(self, table, name):
		q = self._conn.cursor()
		q.execute("SELECT id FROM "+table+" WHERE name = ?", (name,))
		data = q.fetchone()
		if data is None:
			q.execute(
			"INSERT INTO "+table+"(name) VALUES (?)", (name,))
			return q.lastrowid
		else:
			return data[0]
	def getCTime(self, path):
		q = self._conn.cursor()
		q.execute("SELECT id,filectime FROM songs WHERE path = ?",(path,))
		data = q.fetchone()
		return data if data is not None else (0,0)
