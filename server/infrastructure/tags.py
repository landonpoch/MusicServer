import ntpath
import eyed3
from server.domain.entities import Song

class Tags:
    def get_file_info(self, path):
        filename = ntpath.basename(path)
        track = eyed3.core.load(path)
        song = Song()
        if track != None:
            song.has_tags = True
            song.artist = track.tag.artist if track.tag != None else 'unknown'
            song.album = track.tag.album if track.tag != None else 'unknown'
            song.title = track.tag.title if track.tag != None else filename
            song.track = track.tag.track_num[0] if track.tag != None else 0
        else:
            song.title = filename
        return song

    def get_songs(self, path):
        filename = ntpath.basename(path)
        track = eyed3.core.load(path)

        
