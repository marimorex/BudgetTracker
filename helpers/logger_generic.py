import logging
import json
from contextvars import ContextVar


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_name = service_name

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "service_name": self.service_name,  # Fixed to explicitly use the microservice name
            "module": record.module,
            "path": record.pathname,
            "request_id": getattr(
                record, "request_id", None
            ),  # Dynamically add request_id
        }
        return json.dumps(log_record)


# Use a ContextVar to store the request_id per request
request_id_context = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        # Attach the current request_id to the log record
        record.request_id = request_id_context.get()
        return True


def setup_logger(service_name):
    """
    Configures and returns a logger with the given service name.

    :param service_name: Name of the microservice (e.g., 'account_service')
    :return: Configured logger instance
    """
    logger = logging.getLogger(
        service_name
    )  # Ensures logger is tied to the microservice name
    logger.setLevel(logging.INFO)

    if (
        not logger.hasHandlers()
    ):  # Prevents duplicate handlers in case of multiple imports
        handler = logging.StreamHandler()  # Logs to console
        handler.setFormatter(JsonFormatter(service_name=service_name))
        # Add the filter to the handler
        handler.addFilter(RequestIdFilter())
        logger.addHandler(handler)

    return logger
