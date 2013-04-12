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
