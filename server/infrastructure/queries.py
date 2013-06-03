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

    GET_ARTIST_ID = '''SELECT Id
    FROM Artist
    WHERE `Name` = %s'''

    INSERT_ARTIST = '''INSERT INTO Artist
    (Name) VALUES (%s)'''

    GET_ALBUM_ID = '''SELECT Id
    FROM Album
    WHERE `Name` = %s
    AND ArtistId = %s'''

    INSERT_ALBUM = '''INSERT INTO Album
    (Name, ArtistId) VALUES (%s, %s)'''

    INSERT_SONGER = '''INSERT INTO Track
    (Path, Name, Track, AlbumId, LibraryId)
    VALUES (%s, %s, %s, %s, %s)'''
