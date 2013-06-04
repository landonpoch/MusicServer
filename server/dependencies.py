from infrastructure.services import Services
from infrastructure.importer import FileImporter
from infrastructure.mapper import Mapper

class Factory:
    def get_services(self):
        return Services(FileImporter(), Mapper())
