class Artist:
    def __init__(self, library, name):
        self.library = library
        self.name = name

class Album:
    def __init__(self, artist, name):
        self.artist = artist
        self.name = name

class Songer:
    def __init__(self, album, track, title):
        self.album = album
        self.track = track
        self.title = title

class Song:
    def __init__(self):
        self.artist = None
        self.album = None
        self.title = None
        self.track = 0
        self.has_tags = False

class Library:
    def __init__(self, name, path):
        self.name = name
        self.path = path
