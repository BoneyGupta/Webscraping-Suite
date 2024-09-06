import logging
import os
import time


class Logging:
    def __init__(self, filename, details: bool):
        print("Log: " + filename)
        # Create a log file for reports
        self.filename = filename
        # Create a separate logger for each instance
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler for the logger
        handler = logging.FileHandler(filename, mode="w")
        if details:
            handler.setFormatter(logging.Formatter("%(asctime)s -%(levelname)s - %(message)s"))
        else:
            handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
