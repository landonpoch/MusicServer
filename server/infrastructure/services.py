import os
import connection
import repo
import mapper
from server.domain.entities import Library

static_url = '/home/landon/bin/python/django/music/server/static/'

class Services:
    def __init__(self, importer):
        self._importer = importer

    def create_library(self, name, path):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            library = Library(name, path)
            library_id = repository.add_library(library)
            songs = self._importer.recurse_directory(path)
            response = repository.add_songs(songs, library_id)
            conn.commit()
            return response

    def get_libraries(self):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            return repository.get_libraries()

    def get_random(self, count, library_id):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            return repository.get_random_songs(count, library_id)

    def search_songs(self, search_term):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            return repository.search_songs(search_term)

    def get_song_path(self, song_id):
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            return repository.get_song_path(song_id)

    def import_library(self, name, path):
        songs = self._importer.recurse_directory(path)
        artists = mapper.Mapper().map_songs(songs)
        with connection.ConnectionManager() as conn:
            repository = repo.Repo(conn)
            library = Library(name, path)
            library_id = repository.add_library(library)
            repository.add_artists(artists, library_id)
            conn.commit()
        return artists
