import os
import tags

class FileImporter:
    encodings = ['utf-8', 'iso-8859-1']

    def recurse_directory(self, path):
        songs = []
        for root, sub_folders, files in os.walk(path):
            #root = self.get_utf8_string(root)
            for file in [f for f in files if f.endswith('.mp3')]:
                #file = self.get_utf8_string(file)
                fullpath = os.path.join(root, file)
                song = tags.Tags().get_file_info(fullpath)
                song.path = fullpath#(fullpath).replace(path.encode('utf-8') + '/'.encode('utf-8'), '')
                songs.append(song)
        return songs

    def get_utf8_string(self, value):
        for encoding in self.encodings:
            try:
                # Need to preserve encoding so that it can be accessed on the file system correctly
                value = value.decode(encoding)
                value = value.encode('utf-8')
                break
            except:
                continue
        return value
