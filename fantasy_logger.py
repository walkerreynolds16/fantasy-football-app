import logging
from logging import Logger, handlers

class Fantasy_Logger(logging.Logger):

    def __init__(self, name, level=logging.INFO):
        super(Fantasy_Logger, self).__init__(name)
        self.name = name
        self.level = level

        self.setLevel(self.level)
        
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)
