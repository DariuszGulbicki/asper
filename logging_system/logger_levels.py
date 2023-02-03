from enum import Enum

class LoggerLevels(Enum):

    TEXT = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


def from_int(value):
    if isinstance(value, LoggerLevels):
        return value
    if value == 0:
        return LoggerLevels.TEXT
    elif value == 1:
        return LoggerLevels.DEBUG
    elif value == 2:
        return LoggerLevels.INFO
    elif value == 3:
        return LoggerLevels.WARNING
    elif value == 4:
        return LoggerLevels.ERROR
    elif value == 5:
        return LoggerLevels.CRITICAL
    else:
        return None

def to_int(level):
    if isinstance(level, int):
        return level
    if level == LoggerLevels.TEXT:
        return 0
    elif level == LoggerLevels.DEBUG:
        return 1
    elif level == LoggerLevels.INFO:
        return 2
    elif level == LoggerLevels.WARNING:
        return 3
    elif level == LoggerLevels.ERROR:
        return 4
    elif level == LoggerLevels.CRITICAL:
        return 5
    else:
        return None