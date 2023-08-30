import logging

from pythonjsonlogger import jsonlogger

from .settings import get_settings, LogFormat


def init_logging():
    settings = get_settings()
    log_handlers = None
    if settings.log_format == LogFormat.JSON:
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
