class Mapper:
    def map_songs(self, songs):
        artists = {}
        for song in songs:
            self._add_artist(artists, song)
        return artists

    def _add_artist(self, artists, song):
        if song.artist not in artists:
            artists[song.artist] = {}
        self._add_album(artists[song.artist], song)
        del(song.artist)

    def _add_album(self, albums, song):
        if song.album not in albums:
            albums[song.album] = []
        albums[song.album].append(song)
        del(song.album)
