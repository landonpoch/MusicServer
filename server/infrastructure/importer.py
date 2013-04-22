import os
import tags

class FileImporter:
    def recurse_directory(self, path):
        songs = []
        for root, sub_folders, files in os.walk(path):
            for file in [f for f in files if f.endswith('.mp3')]:
                fullpath = os.path.join(root, file)
                song = tags.Tags().get_file_info(fullpath)
                song.path = os.path.relpath(fullpath, path)
                songs.append(song)
        return songs
