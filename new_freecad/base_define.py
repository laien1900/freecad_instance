from enum import Enum


class command_type(Enum):
    NONE_TYPE = -1
    ERROR_MESSAGE = 0
    REGISTER_SERVICE = 1
    NEW_INSTANCE = 2
    CLOSE_INSTANCE = 3
    DELAY_TIME = 4,


class instance_status(Enum):
    PENGING = 0
    RUNING = 1
    CLOSED = 2


def MessageProcess(id):
    return command_type(id)