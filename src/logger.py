import logging
from data import LOGGER_FORMAT, LOGGER_DATE_FORMAT


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name=name)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt=logging.Formatter(fmt=LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT))
        file_handler = logging.FileHandler(filename=name + ".log")
        self.addHandler(stream_handler)
        self.addHandler(file_handler)
