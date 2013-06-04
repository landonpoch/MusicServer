import os

import connection
import repo
import mapper
from server.domain import entities
from server.models import Library, Artist, Album, Song

static_url = '/home/landon/bin/python/django/music/server/static/'

class Services:
    def __init__(self, importer, mapper):
        self._importer = importer
        self._mapper = mapper

    '''
    This is now using django models instead of custom database code.
    However, might need to look into atomicity for these db operations.
    '''
    def create_library(self, name, path):
        library = Library(name=name, path=path)
        library.save()
        songs = self._importer.recurse_directory(path)
        artists = self._mapper.map_songs(songs)
        self._add_artists(artists, library)

    def _add_artists(self, artists, library):
        for name, albums in artists.iteritems():
            name = name if name is not None else 'unknown'
            artist = Artist(name=name)
            artist.save()
            self._add_albums(artist, albums, library)

    def _add_albums(self, artist, albums, library):
        for name, songs in albums.iteritems():
            name = name if name is not None else 'unknown'
            album = Album(name=name, artist=artist)
            album.save()
            for s in songs:
                song_name = s.title if s.title is not None else 'unknown'
                song = Song(relative_path = s.path,
                    name=song_name, 
                    track=s.track, 
                    album=album, 
                    library=library)
                song.save()


    def get_libraries(self):
        return Library.objects.all()

    def get_random(self, count, library_id):
        songs = Song.objects.filter(library_id=library_id).order_by('?')[:count]
        return self._map_songs(songs)

    def _map_songs(self, songs):
        for song in songs:
            s = entities.Song()
            s.mp3 = 'stream_song?id=%s' % song.id
            s.title = song.name
            s.artist = song.album.artist.name
            yield s
    
    def search_songs(self, search_term):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            return repository.search_songs(search_term)

    def get_song_path(self, song_id):
        song = Song.objects.get(pk=song_id)
        return os.path.join(song.library.path, song.relative_path)

    def import_library(self, name, path):
        songs = self._importer.recurse_directory(path)
        artists = self._mapper.map_songs(songs)
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            library = Library(name, path)
            library_id = repository.add_library(library)
            repository.add_artists(artists, library_id)
            conn.commit()
        return artists
