

class CsvStorageHelper:
    __sinkDirectory = None

    def __init__(self, settings):
        csvStorageSettings = settings.CsvStorageHelper
        CsvStorageHelper.__sinkDirectory = csvStorageSettings["SinkDirectory"]