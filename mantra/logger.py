import logging

from colorlog import ColoredFormatter


LOG_LEVEL = logging.DEBUG
LOGFORMAT = (
    "[%(log_color)s%(levelname)s%(reset)s] "
    "%(log_color)s%(message)s%(reset)s"
)


def get_logger(name, level=LOG_LEVEL, log_format=LOGFORMAT):
    logging.root.setLevel(level)
    formatter = ColoredFormatter(log_format)
    stream = logging.StreamHandler()
    stream.setLevel(level)
    stream.setFormatter(formatter)
    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(stream)
    return log
