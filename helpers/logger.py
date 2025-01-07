from helpers.logger_generic import setup_logger, request_id_context
import os


class Logger:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = setup_logger(os.getenv("SERVICE_NAME"))
        return self._instance


logger = Logger()
