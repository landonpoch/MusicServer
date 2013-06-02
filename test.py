from server.infrastructure.services import Services
from server.infrastructure.importer import FileImporter

service = Services(FileImporter())
artists = service.import_library('test', '/home/landon/Music/Regular/Assorted')
