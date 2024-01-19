import logging
from logging import Logger

from app.settings import settings


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)

    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)

    return logger
