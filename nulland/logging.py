import logging

from pythonjsonlogger import jsonlogger

from .config import settings


def init_logging():
    log_handlers = None
    if settings.log_format == settings.LogFormat.JSON:
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            "%(levelname)s %(name)s %(message)s",
            rename_fields={"levelname": "severity", "name": "component"},
        )
        handler.setFormatter(formatter)
        log_handlers = [handler]
    logging.basicConfig(handlers=log_handlers)
    logger = logging.getLogger("nulland")
    logger.setLevel(logging.INFO)
