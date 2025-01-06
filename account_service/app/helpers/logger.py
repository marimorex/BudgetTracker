from helpers.logger_generic import setup_logger, request_id_context


class Logger:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = setup_logger(
                "account_service"
            )  # todo use later ENV variables
        return self._instance


logger = Logger()
