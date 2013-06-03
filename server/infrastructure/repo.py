import os
import MySQLdb

from queries import Queries
from server.domain.entities import Song, Library

class Repo:
    def __init__(self, conn):
        self._conn = conn

    def add_library(self, library):
        cursor = self._conn.cursor()
        cursor.execute(Queries.INSERT_LIBRARY, (library.name, library.path))
        return cursor.lastrowid

    def get_libraries(self):
        cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(Queries.GET_LIBRARIES)
        libraries = []
        for record in cursor.fetchall():
            libraries.append(Library(record['Name'], record['Path']))
        return libraries

    def get_random_songs(self, count, library_id):
        cursor = self._conn.cursor()
        query = Queries.RANDOM_SONGS % (library_id, str(count))
        cursor.execute(query)
        return self._load_songs(cursor)

    def search_songs(self, search_term):
        cursor = self._conn.cursor()
        query = Queries.SEARCH_SONGS % ((search_term,) * 4)
        cursor.execute(query)
        return self._load_songs(cursor)
    
    def get_song_path(self, song_id):
        cursor = self._conn.cursor()
        query = Queries.GET_PATH_BY_ID % song_id
        cursor.execute(query)
        for record in cursor.fetchall():
            return os.path.join(record[0], record[1])
    
    def add_songs(self, songs, library_id):
        for song in songs:
            self._add_song(song, library_id)

    def add_artists(self, artists, library_id):
        for name, artist in artists.iteritems():
            self._add_artist(name, artist, library_id)

    def _add_song(self, song, library_id):
        cursor = self._conn.cursor()
        print 'inserting %s into database...' % song.path
        cursor.execute(Queries.INSERT_SONG, 
        (song.path, song.title, song.album, 
        song.artist, song.track, library_id))

    def _add_artist(self, name, artist, library_id):
        cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
        name = name or 'Unknown Artist'
        cursor.execute(Queries.GET_ARTIST_ID, name)
        result = cursor.fetchone()
        artist_id = result['Id'] if result else None
        if not artist_id:
            cursor.execute(Queries.INSERT_ARTIST, name)
            artist_id = cursor.lastrowid
        print 'Artist %s:  %s' % (artist_id, name)
        for album_name, album in artist.iteritems():
            self._add_album(cursor, album_name, album, artist_id, library_id)

    def _add_album(self, cursor, name, album, artist_id, library_id):
        cursor.execute(Queries.GET_ALBUM_ID, (name, artist_id))
        result = cursor.fetchone()
        album_id = result['Id'] if result else None
        if not album_id:
            cursor.execute(Queries.INSERT_ALBUM, (name, artist_id))
            album_id = cursor.lastrowid
        print '  Album %s: %s' % (album_id, name)
        for song in album:
            self._add_songer(cursor, song, album_id, library_id)

    def _add_songer(self, cursor, song, album_id, library_id):
        cursor.execute(Queries.INSERT_SONGER, (song.path, song.title, song.track, album_id, library_id))
        print '    Track %s: %s' % (cursor.lastrowid, song.title)

    def _load_songs(self, cursor):
        songs = []
        for record in cursor.fetchall():
            song = Song()
            song.path = 'stream_song?id=%s' % record[0]
            song.title = record[1]
            song.artist = record[2]
            songs.append(song)
        return songs
