from infrastructure.services import Services
from infrastructure.importer import FileImporter

class Factory:
    def get_services(self):
        return Services(FileImporter())
