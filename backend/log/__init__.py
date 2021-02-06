from pytz import timezone, utc
from datetime import datetime
import logging
import sys
import config

LEVEL = "INFO"
if config.DEBUG:
    LEVEL = "DEBUG"

LOGS_FORMAT = "%(asctime)s — %(name)s — %(levelname)s - %(process)d " \
              "- %(thread)d — %(funcName)s:%(lineno)d — %(message)s"


def set_logger_level(level):
    """
    set log level
    :param level: str
    :return None
    """
    global LEVEL
    LEVEL = level


def get_logger_level():
    """
    get log level
    :return: str
    """
    return LEVEL


def custom_time(*_args):
    """
    get the customised time
    :param _args: datetime arguments
    :return: time.struct_time
    """
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Asia/Kolkata")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def get_logger(name):
    """
    get the customised logger for the given python file
    :param name: str
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    logging.Formatter.converter = custom_time
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOGS_FORMAT))
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    pass
