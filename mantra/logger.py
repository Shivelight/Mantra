import logging

from colorlog import ColoredFormatter

LOGGER = {}
LOG_LEVEL = logging.DEBUG
LOGFORMAT = (
    "[%(log_color)s%(levelname)s%(reset)s] "
    "%(log_color)s%(message)s%(reset)s"
)


def get_logger(name):
    """Returns specific logger instance."""
    try:
        return LOGGER[name]
    except KeyError:
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        log = logging.getLogger(name)
        log.setLevel(LOG_LEVEL)
        log.addHandler(stream)

        # Store the logger to avoid duplicate handler which causing duplicate
        # message and return it later when same logger is asked.
        LOGGER[name] = log
        return log
