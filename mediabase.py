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
		filemtime DATETIME
		);
	CREATE UNIQUE INDEX IF NOT EXISTS pathidx ON songs (path,filemtime);
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
		q = self._conn.cursor()
		q.execute("SELECT path, filemtime FROM songs WHERE path = ?;", (mo['path'],))
		data = q.fetchone()
		if data is not None:
			if mo['mtime'] > data[1]:
				raise NotImplementedError('re-adding existing data not yet supported')
			else:
				return
		for key in ['album', 'title', 'artist', 'genre']:
			if key not in mo.keys():
				mo[key]=['Unknown']
		mo['album'] = self.getId('albums', mo['album'][0])
		rows = "album,name,path,filemtime"
		parameters = '?,?,?,?'
		values = ( mo['album'], mo['title'][0], mo['path'], mo['mtime'])
		if 'track-number' in mo.keys():
			rows = rows+',trackno'
			parameters = parameters+',?'
			values = values + (mo['track-number'][0],)
		q.execute("INSERT INTO songs("+rows+") VALUES ("+parameters+")", values)
		song_id = q.lastrowid
		for artist in mo['artist']:
			artist = self.getId('artists',artist)
			q.execute("INSERT INTO song_artists VALUES (?, ?, ?)", (song_id, artist, 1))
		for genre in mo['genre']:
			genre = self.getId('genres',genre)
			q.execute("INSERT INTO song_genres VALUES (?, ?)", (song_id, genre))
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
