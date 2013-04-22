import os
import MySQLdb

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

    def _add_song(self, song, library_id):
        cursor = self._conn.cursor()
        print 'inserting %s into database...' % song.path
        cursor.execute(Queries.INSERT_SONG, 
        (song.path, song.title, song.album, 
        song.artist, song.track, library_id))

    def _load_songs(self, cursor):
        songs = []
        for record in cursor.fetchall():
            song = Song()
            song.path = 'stream_song?id=%s' % record[0]
            song.title = record[1]
            song.artist = record[2]
            songs.append(song)
        return songs
        

class Queries:
    INSERT_LIBRARY = '''INSERT INTO Library
    (Name, Path)
    VALUES (%s, %s)'''

    GET_LIBRARIES = '''SELECT Id, `Name`, Path
    FROM Library'''

    INSERT_SONG = '''INSERT INTO Song
    (RelativePath, Title, Album, Artist, Track, LibraryId)
    VALUES (%s, %s, %s, %s, %s, %s)'''

    RANDOM_SONGS = '''SELECT 
        s.Id, 
        s.Title,
        s.Artist
    FROM Song s
    INNER JOIN Library l ON s.LibraryId = l.Id
    WHERE LibraryId = %s
    ORDER BY RAND()
    LIMIT 0, %s'''

    SEARCH_SONGS = '''SELECT
        s.Id,
        s.Title,
        s.Artist
    FROM Song s
    INNER JOIN Library l ON s.LibraryId = l.Id
    WHERE 
    (UPPER(s.Title) LIKE UPPER('%%%s%%')
    OR UPPER(s.Album) LIKE UPPER('%%%s%%')
    OR UPPER(s.Artist) LIKE UPPER('%%%s%%')
    OR UPPER(s.RelativePath) LIKE UPPER('%%%s%%'))'''

    GET_PATH_BY_ID = '''SELECT 
        l.Path, 
        s.RelativePath
    FROM Library l
    INNER JOIN Song s ON l.Id = s.LibraryId
    WHERE s.Id = %s'''
