from .base_importer import BaseImporter as BaseImporter
from .csv_importer import CsvImporter
from .json_importer import JsonImporter
from .xlsx_importer import XlsxImporter
from .yaml_importer import YamlImporter

IMPORTERS = [
    JsonImporter(),
    YamlImporter(),
    CsvImporter(),
    XlsxImporter()
]
