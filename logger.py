from abc import ABC, abstractmethod
import logging

class Logger(ABC):
    @abstractmethod
    def warning(self, document_filename, line_number):
        pass

class FileLogger(Logger):
    def __init__(self, log_filename):
       self.logger = logging.getLogger(log_filename)
       self.logger.setLevel(logging.WARNING)
       self.logger.propagate = False

       if not self.logger.handlers:
           handler = logging.FileHandler(log_filename,
                                         mode="a",
                                         encoding="utf-8")
           handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
           self.logger.addHandler(handler)

    def warning(self, document_filename, line_number, duplicate=False):
        if duplicate:
            self.logger.warning("Duplicate key at %s in %s", line_number, document_filename)
        else:
            self.logger.warning("Line %s is malformed in %s", line_number, document_filename)
            
        

    